

#include "RigUnit_SetGizmoVisibility.h"
#include "Units/RigUnitContext.h"

FRigUnit_SetGizmoVisibility_Execute()
{
    DECLARE_SCOPE_HIERARCHICAL_COUNTER_RIGUNIT(  )
    FRigControlHierarchy* Hierarchy = ExecuteContext.GetControls();
    if (Hierarchy)
    {
        switch (Context.State)
        {
            case EControlRigState::Init:
                {
                    CachedControlIndex = Hierarchy->GetIndex(Control);
                    break;
                }
            case EControlRigState::Update:
                {
                    if (CachedControlIndex != INDEX_NONE)
                    {
                        /** This does not work for whatever reason. Who knows. **/
                        FRigControl Ctl = (*Hierarchy)[CachedControlIndex];
                        if (Ctl.ControlType != ERigControlType::Bool)
                        {
                            Ctl.bGizmoEnabled = Visibility;
                        }
                    }
                    break;
                }
            default:
                {
                    break;
                }
        }
    }
}