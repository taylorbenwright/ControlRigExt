

#include "RigUnit_GetGizmoVisibility.h"
#include "Units/RigUnitContext.h"

FRigUnit_GetGizmoVisibility_Execute()
{
    DECLARE_SCOPE_HIERARCHICAL_COUNTER_RIGUNIT(  )
    const FRigControlHierarchy* Hierarchy = Context.GetControls(  );
    if (Hierarchy)
    {
        switch (Context.State)
        {
        case EControlRigState::Init:
            {
                CachedControlIndex = Hierarchy->GetIndex(Control);
            }
        case EControlRigState::Update:
            {
                if (CachedControlIndex != INDEX_NONE)
                {
                    Visibility = (*Hierarchy)[CachedControlIndex].bGizmoEnabled;
                }
            }
        default:
            {
                break;
            }
        }
    }
}