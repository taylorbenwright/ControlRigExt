// Copyright Technically Games, LLC

#pragma once

#include "ControlRig/Public/Units/RigUnit.h"
#include "RigUnit_GetGizmoVisibility.generated.h"

/**
* GetGizmoVisibility returns the current Visibility of a Controller's gizmo
**/
USTRUCT(meta=(DisplayName="Get Gizmo Visibility", Category="Controls Ext", Keywords="GetGizmoVisibility"))
struct FRigUnit_GetGizmoVisibility : public FRigUnit
{
    GENERATED_BODY()

    FRigUnit_GetGizmoVisibility()
        : Visibility(false)
        , CachedControlIndex(INDEX_NONE)
    {}

    RIGVM_METHOD(  )
    virtual void Execute(const FRigUnitContext& Context) override;

    UPROPERTY(meta= (Input, CustomWidget = "ControlName", Constant))
    FName Control;

    UPROPERTY(meta=(Output))
    bool Visibility;

    // Used to cache the internally used bone index
    UPROPERTY()
    int32 CachedControlIndex;
};