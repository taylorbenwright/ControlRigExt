// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class ControlRigExt : ModuleRules
{
	public ControlRigExt(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;
		
		PrivateIncludePaths.Add("ControlRigExt/Private");
		PrivateIncludePaths.Add("ControlRigExt/Private/Units");

		PublicDependencyModuleNames.AddRange(
			new string[]
			{
				"AnimationCore",
				"LevelSequence",
				"RigVM",
				"ControlRig"
			}
		);
		
		PrivateDependencyModuleNames.AddRange(
			new string[]
			{
				"Core",
				"CoreUObject",
				"Engine",
				"AnimGraphRuntime",
				"MovieScene",
				"MovieSceneTracks",
				"PropertyPath",
				"TimeManagement",
			}
		);


		if (Target.bBuildEditor == true)
		{
			PublicDependencyModuleNames.AddRange(
				new string[]
				{
					"RigVMDeveloper",
					"AnimGraph",
				}
			);

			PrivateDependencyModuleNames.AddRange(
				new string[]
				{
					"UnrealEd",
					"BlueprintGraph",
					"PropertyEditor",
					"RigVMDeveloper",
				}
			);

			PrivateIncludePathModuleNames.Add("ControlRigEditor");
			DynamicallyLoadedModuleNames.Add("ControlRigEditor");
		}
	}
}
