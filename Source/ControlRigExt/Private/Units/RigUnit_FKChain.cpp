

#include "RigUnit_FKChain.h"
#include "Units/RigUnitContext.h"

FRigUnit_FKChain_Execute()
{
    DECLARE_SCOPE_HIERARCHICAL_COUNTER_RIGUNIT()
    FRigBoneHierarchy* Hierarchy = ExecuteContext.GetBones();
    if (Hierarchy)
    {
        switch (Context.State)
        {
        case EControlRigState::Init:
            {                
                for (int i = 0; i < JointControllerPairs.Num(  ); i++)
                {
                    FRigUnit_FKChain_JointControllerPair& Pair = JointControllerPairs[i];
                    
                    Pair.CachedBoneIndex = Hierarchy->GetIndex( Pair.Bone );
                    
                    Hierarchy->GetChildren( Pair.CachedBoneIndex, Pair.ValidChildren, true );
                    if (i > 0)
                    {
                        if (!JointControllerPairs[i-1].ValidChildren.Contains( Pair.CachedBoneIndex ))
                        {
                            UE_CONTROLRIG_RIGUNIT_REPORT_WARNING( TEXT("All FK Chain Bones must be in a single chain."));
                            return;
                        }
                    }
                }
                return;
            }
        case EControlRigState::Update:
            {
                if (Weight <= SMALL_NUMBER || JointControllerPairs.Num(  ) < 1 )
                {
                    return;
                }
                for (FRigUnit_FKChain_JointControllerPair& Pair : JointControllerPairs)
                {
                    if (Pair.CachedBoneIndex != INDEX_NONE)
                    {
                        switch (Pair.Space)
                        {
                            case EBoneGetterSetterMode::GlobalSpace:
                                {
                                    if (FMath::IsNearlyEqual( Weight, 1.f ))
                                    {
                                        Hierarchy->SetGlobalTransform( Pair.Bone,
                                                                       Pair.Transform,
                                                                       Pair.bPropagateToChildren );
                                    }
                                    else
                                    {
                                        float T = FMath::Clamp<float>(Weight, 0.f, 1.f);
                                        const FTransform PreviousTransform = Hierarchy->GetGlobalTransform( Pair.Bone );
                                        Hierarchy->SetGlobalTransform( Pair.Bone,
                                                                       FControlRigMathLibrary::LerpTransform( PreviousTransform, Pair.Transform, T ),
                                                                       Pair.bPropagateToChildren);
                                    }
                                    break;
                                }
                            case EBoneGetterSetterMode::LocalSpace:
                                {
                                    if (FMath::IsNearlyEqual(Weight, 1.f))
                                    {
                                        Hierarchy->SetLocalTransform(Pair.Bone,
                                                                     Pair.Transform,
                                                                     Pair.bPropagateToChildren);
                                    }
                                    else
                                    {
                                        float T = FMath::Clamp<float>(Weight, 0.f, 1.f);
                                        const FTransform PreviousTransform = Hierarchy->GetLocalTransform(Pair.Bone);
                                        Hierarchy->SetLocalTransform(Pair.Bone,
                                                                     FControlRigMathLibrary::LerpTransform(PreviousTransform, Pair.Transform, T),
                                                                     Pair.bPropagateToChildren);
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
            }
        default:
            {
                break;
            }
        }
    }
}
