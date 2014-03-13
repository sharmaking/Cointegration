//////////////////////////////////////////////////////////////////////////
// LiYun, 2014 - 2014
//////////////////////////////////////////////////////////////////////////

#ifndef __MRDCORP_MrdDef_CorpMath_H__
#define __MRDCORP_MrdDef_CorpMath_H__

#ifndef MRDCORPMATH_DLLAPI
	#ifdef __MRDCORPMATH_DLL_BUILD
		#define MRDCORPMATH_DLLAPI		__declspec(dllexport)
	#else // _USRDLL
		#define MRDCORPMATH_DLLAPI		__declspec(dllimport)
	#endif // _USRDLL
#endif // MRDCORP_DLLAPI

#define MRDCORPMATH_API		__stdcall

#endif // __MRDCORP_MrdDef_CorpMath_H__
