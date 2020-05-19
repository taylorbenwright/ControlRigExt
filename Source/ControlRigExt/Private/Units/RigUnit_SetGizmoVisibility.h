

#pragma once

#include "ControlRig/Public/Units/RigUnit.h"
#include "RigUnit_SetGizmoVisibility.generated.h"

/**
* SetGizmoVisibility will set the visibility of a Controller's gizmo.
* Note: This does not seem to work as-is. 
**/
USTRUCT(meta=(DisplayName="Set Gizmo Visibility", Category="Controls Ext", Keywords="SetGizmoVisibility", NodeColor = "0.25 0.25 0.05"))
struct FRigUnit_SetGizmoVisibility : public FRigUnitMutable
{
    GENERATED_BODY()

    FRigUnit_SetGizmoVisibility()
        : Visibility(true)
        , CachedControlIndex(INDEX_NONE)
    {}

    RIGVM_METHOD(  )
    virtual void Execute(const FRigUnitContext& Context) override;

    UPROPERTY(meta = (Input, CustomWidget = "ControlName", Constant))
    FName Control;

    UPROPERTY(meta = (Input, Output))
    bool Visibility;

    UPROPERTY()
    int32 CachedControlIndex;
};