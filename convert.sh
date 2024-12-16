#!/bin/bash

class=(
    's/adf\.core\.agent\.Agent/adf_core_python.agent.Agent/g'
    's/adf\.core\.agent\.config\.ModuleConfig/adf_core_python.agent.config.ModuleConfig/g'
    's/adf\.core\.agent\.develop\.DevelopData/adf_core_python.agent.develop.DevelopData/g'
    's/adf\.core\.agent\.info\.AgentInfo/adf_core_python.agent.info.AgentInfo/g'
    's/adf\.core\.agent\.module\.ModuleManager/adf_core_python.agent.module.ModuleManager/g'
    's/adf\.core\.agent\.precompute\.PrecomputeData/adf_core_python.agent.precompute.PrecomputeData/g'
    's/adf\.core\.agent\.precompute\.PreData/adf_core_python.agent.precompute.PreData/g'
    's/adf\.core\.component\.extaction\.ExtAction/adf_core_python.component.extaction.ExtAction/g'
    's/adf\.core\.component\.module\.AbstractModule/adf_core_python.component.module.AbstractModule/g'
    's/adf\.core\.component\.module\.algorithm\.Clustering/adf_core_python.component.module.algorithm.Clustering/g'
    's/adf\.core\.component\.module\.algorithm\.DynamicClustering/adf_core_python.component.module.algorithm.DynamicClustering/g'
    's/adf\.core\.component\.module\.algorithm\.PathPlanning/adf_core_python.component.module.algorithm.PathPlanning/g'
    's/adf\.core\.component\.module\.algorithm\.StaticClustering/adf_core_python.component.module.algorithm.StaticClustering/g'
    's/adf\.core\.component\.module\.complex\.AmbulanceTargetAllocator/adf_core_python.component.module.complex.AmbulanceTargetAllocator/g'
    's/adf\.core\.component\.module\.complex\.BuildingDetector/adf_core_python.component.module.complex.BuildingDetector/g'
    's/adf\.core\.component\.module\.complex\.FireTargetAllocator/adf_core_python.component.module.complex.FireTargetAllocator/g'
    's/adf\.core\.component\.module\.complex\.HumanDetector/adf_core_python.component.module.complex.HumanDetector/g'
    's/adf\.core\.component\.module\.complex\.PoliceTargetAllocator/adf_core_python.component.module.complex.PoliceTargetAllocator/g'
    's/adf\.core\.component\.module\.complex\.RoadDetector/adf_core_python.component.module.complex.RoadDetector/g'
    's/adf\.core\.component\.module\.complex\.Search/adf_core_python.component.module.complex.Search/g'
    's/adf\.core\.component\.module\.complex\.TargetAllocator/adf_core_python.component.module.complex.TargetAllocator/g'
    's/adf\.core\.component\.module\.complex\.TargetDetector/adf_core_python.component.module.complex.TargetDetector/g'
    's/adf\.core\.gateway\.Gateway/adf_core_python.gateway.Gateway/g'
)

for c in "${class[@]}"; do
    find . -type f -name "*.java" -print0 | xargs -0 sed -i "" "$c"
done