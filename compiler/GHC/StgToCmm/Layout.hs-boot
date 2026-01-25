module GHC.StgToCmm.Layout where

import Prelude (Int)
import GHC.Platform.Profile
import GHC.StgToCmm.Closure
import GHC.Core.TyCon

mkVirtConstrOffsets
  :: Profile -> [NonVoid (PrimRep, a)]
  -> (Int, Int, [(NonVoid a, Int)])