module GHC.StgToCmm.Expr where

import GHC.StgToCmm.Monad ( FCode, ReturnKind )
import GHC.Stg.Syntax (CgStgExpr)
import GHC.Hs.Basic (FieldLabelString)
import GHC.Core.TyCo.Rep (Type)
import GHC.Core.TyCon (TyCon)

cgSelectField :: FieldLabelString  -- selected field
              -> CgStgExpr    -- scrutinee
              -> Type         -- ?
              -> TyCon        -- tycon of the data type
              -> [Type]       -- instantiated at these type args
              -> FCode ReturnKind