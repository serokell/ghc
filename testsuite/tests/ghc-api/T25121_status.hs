{-# LANGUAGE RequiredTypeArguments #-}
{-# LANGUAGE ExplicitNamespaces #-}

module Main where

import Data.Kind
import Type.Reflection
import GHC.Hs as T (type GhcPs)
import GHC.Hs

checkExtField :: String -> forall a b -> (Typeable a, Typeable b) => IO ()
checkExtField ctx a b =
  let aRep = typeRep @a
      bRep = typeRep @b
  in case eqTypeRep aRep bRep of
       Nothing    -> do
         putStrLn $ "X" ++ ctx ++ " (mismatch)"
         putStrLn $ "  / " ++ show aRep
         putStrLn $ "  / " ++ show bRep
       Just HRefl -> do
         putStrLn $ "X" ++ ctx ++ " (match) = " ++ show aRep

assertEqExtField :: String -> forall a b -> (Typeable a, a ~ b) => IO ()
assertEqExtField ctx a b = checkExtField ctx a b

main :: IO ()
main = do
  putStrLn "GhcPs"
  putStrLn "-----"
  checkExtField "Var"         (XVar T.GhcPs)      (XTyVar T.GhcPs)
  assertEqExtField "LitE"     (XLitE T.GhcPs)     (XTyLit T.GhcPs)
  assertEqExtField "Par"         (XPar T.GhcPs)      (XParTy T.GhcPs)
  assertEqExtField "App"         (XApp T.GhcPs)      (XAppTy T.GhcPs)
  assertEqExtField "AppTypeE"    (XAppTypeE T.GhcPs) (XAppKindTy T.GhcPs)
  assertEqExtField "OpApp"       (XOpApp T.GhcPs)    (XOpTy T.GhcPs)
  assertEqExtField "ForAll"      (XForAll T.GhcPs)   (XForAllTy T.GhcPs)
  assertEqExtField "Qual"        (XQual T.GhcPs)     (XQualTy T.GhcPs)
  assertEqExtField "Star"        (XStar T.GhcPs)     (XStarTy T.GhcPs)
  assertEqExtField "FunArr"      (XFunArr T.GhcPs)   (XFunTy T.GhcPs)
  assertEqExtField "ExprWithTySig" (XExprWithTySig T.GhcPs) (XKindSig T.GhcPs)
  assertEqExtField "UntypedSplice" (type (XUntypedSplice GhcPs)) (XSpliceTy T.GhcPs)
  checkExtField "ExplicitList"  (XExplicitList T.GhcPs)  (XExplicitListTy T.GhcPs)
  checkExtField "ExplicitTuple" (XExplicitTuple T.GhcPs) (XExplicitTupleTy T.GhcPs)
  checkExtField "Hole"          (XHole T.GhcPs)          (XWildCardTy T.GhcPs)
  -- checkExtField "" () (XListTy T.GhcPs)
  -- checkExtField "" () (XTupleTy T.GhcPs)
  -- checkExtField "" () (XSumTy T.GhcPs)
  -- checkExtField "" () (XIParamTy T.GhcPs)
  -- checkExtField "" () (XDocTy T.GhcPs)