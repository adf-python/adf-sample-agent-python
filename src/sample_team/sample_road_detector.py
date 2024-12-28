from typing import Optional, cast

from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.component.module.algorithm.clustering import Clustering
from adf_core_python.core.component.module.algorithm.path_planning import PathPlanning
from adf_core_python.core.component.module.complex.road_detector import RoadDetector
from adf_core_python.core.logger.logger import get_agent_logger
from rcrs_core.connection.URN import Entity as EntityURN
from rcrs_core.entities.ambulanceTeam import AmbulanceTeam
from rcrs_core.entities.area import Area
from rcrs_core.entities.civilian import Civilian
from rcrs_core.entities.entity import Entity
from rcrs_core.entities.fireBrigade import FireBrigade
from rcrs_core.entities.human import Human
from rcrs_core.entities.policeForce import PoliceForce
from rcrs_core.worldmodel.entityID import EntityID


class SampleRoadDetector(RoadDetector):
    def __init__(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        develop_data: DevelopData,
    ) -> None:
        super().__init__(
            agent_info, world_info, scenario_info, module_manager, develop_data
        )
        self._opened_areas: set[Area] = set()
        self._clustering: Clustering = cast(
            Clustering,
            module_manager.get_module(
                "SampleRoadDetector.Clustering",
                "adf_core_python.implement.module.algorithm.k_means_clustering.KMeansClustering",
            ),
        )
        self._path_planning: PathPlanning = cast(
            PathPlanning,
            module_manager.get_module(
                "SampleRoadDetector.PathPlanning",
                "adf_core_python.implement.module.algorithm.a_star_path_planning.AStarPathPlanning",
            ),
        )
        self.register_sub_module(self._clustering)
        self.register_sub_module(self._path_planning)

        self._result: Optional[EntityID] = None
        self._logger = get_agent_logger(
            f"{self.__class__.__module__}.{self.__class__.__qualname__}",
            self._agent_info,
        )

    def calculate(self) -> RoadDetector:
        position_id: EntityID = self._agent_info.get_position_entity_id()
        current_position: Area = cast(Area, self._world_info.get_entity(position_id))
        self._opened_areas.add(current_position)

        if position_id == self._result:
            self._logger.debug(f"Reached to {current_position}, resetting target")
            self._result = None

        if self._result is None:
            current_targets: set[Area] = self._calc_targets()
            self._logger.debug(f"Targets: {current_targets}")
            if not current_targets:
                self._result = None
                return self

            nearest_target: Area = min(
                current_targets,
                key=lambda target: self._world_info.get_distance(
                    position_id, target.get_id()
                ),
            )

            path: list[EntityID] = self._path_planning.get_path(
                position_id, nearest_target.get_id()
            )
            if path:
                self._result = path[-1]
            self._logger.debug(f"Selected Target: {self._result}")

        return self

    def _calc_targets(self) -> set[Area]:
        target_areas: set[Area] = set()

        for entity in self._world_info.get_entities_of_types(
            [
                Civilian,
                AmbulanceTeam,
                FireBrigade,
                PoliceForce,
            ]
        ):
            if self._is_valid_human(entity):
                human: Human = cast(Human, entity)
                target_areas.add(
                    cast(Area, self._world_info.get_entity(human.get_position()))
                )

        if len(target_areas) == 0:
            for entity in self._world_info.get_entities_of_types([Area]):
                if isinstance(entity, Area) and entity.get_blockades():
                    target_areas.add(cast(Area, entity))

        target_areas.difference_update(self._opened_areas)

        return target_areas

    def _filter_in_cluster(self, target_areas: set[Area]) -> set[Area]:
        cluster_index: int = self._clustering.get_cluster_index(
            self._agent_info.get_entity_id()
        )
        in_cluster: set[Area] = {
            cast(Area, entity)
            for entity in self._clustering.get_cluster_entities(cluster_index)
        }
        return {area for area in target_areas if area in in_cluster}

    def _is_valid_human(self, entity: Entity) -> bool:
        if not isinstance(entity, Human):
            return False
        human: Human = cast(Human, entity)
        if human.get_hp() is None or human.get_hp() == 0:
            return False
        if not human.get_position():
            return False
        if human.damage is None or human.damage == 0:
            return False
        if human.get_buriedness() is not None:
            return False

        position: Optional[Entity] = self._world_info.get_entity(human.get_position())
        if position is None:
            return False

        urn: EntityURN = position.get_urn()
        if urn in {EntityURN.REFUGE, EntityURN.AMBULANCE_TEAM}:
            return False

        return True

    def get_target_entity_id(self) -> Optional[EntityID]:
        return self._result
