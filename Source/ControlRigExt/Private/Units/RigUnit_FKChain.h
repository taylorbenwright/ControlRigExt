#pragma once

#include "ControlRig/Private/Units/Highlevel/RigUnit_HighlevelBase.h"
#include "RigUnit_FKChain.generated.h"

USTRUCT()
struct FRigUnit_FKChain_JointControllerPair
{
    GENERATED_BODY( )

    /**
    * The name of the Bone to set the transform for.
    */
    UPROPERTY(meta = (Input, Constant, CustomWidget = "BoneName"))
    FName Bone;

    /**
    * The transform value to set for the given Bone.
    */
    UPROPERTY(meta = (Input, Output))
    FTransform Transform;

    /**
    * Defines if the bone's transform should be set
    * in local or global space.
    */
    UPROPERTY(meta = (Input))
    EBoneGetterSetterMode Space;

    /**
    * If set to true all of the global transforms of the children
    * of this bone will be recalculated based on their local transforms.
    * Note: This is computationally more expensive than turning it off.
    */
    UPROPERTY(meta = (Input, Constant))
    bool bPropagateToChildren = true;

    int32 CachedBoneIndex;
    TArray<int32> ValidChildren;
};

/**
* Applies a simple FK chain to a joint chain without the needs for extra nodes
*/
USTRUCT(meta=(DisplayName="FK Chain", Category="Controls Ext", Keywords="FK,Chain"))
struct FRigUnit_FKChain : public FRigUnit_HighlevelBaseMutable
{
    GENERATED_BODY()

    RIGVM_METHOD()
    virtual void Execute(const FRigUnitContext& Context) override;

    FRigUnit_FKChain()
    {
        Weight = 1.f;
    }

    /**
     * The joint/controller pairs that should be coupled. Each successive joint MUST
     * be lower in the hierarchy than the previous.
     */
    UPROPERTY(meta=(Input))
    TArray<FRigUnit_FKChain_JointControllerPair> JointControllerPairs;

    /** 
    * The weight of the chain - how much of the FK should be applied
    */
    UPROPERTY(meta = (Input, UIMin = "0.0", UIMax = "1.0"))
    float Weight;
    
};