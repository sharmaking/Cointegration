
#ifndef __MRDCORP_MrdCorpDef_H__
#define __MRDCORP_MrdCorpDef_H__

#if defined(_M_IA64)
	#define _MRDCORP_IA64
	#define MRDCORP_IA64		1
	#define MRDCORP_X64			1
#elif defined(_WIN64)
	#define _MRDCORP_X64
	#define MRDCORP_X64			1
#elif defined(_WIN32)
	#define _MRDCORP_X32
	#define MRDCORP_X32			1
#else
	#error "Platform is unknown."
#endif

// the definition for NULL
#ifndef NULL
	#ifdef __cplusplus
		#define NULL	0
	#else
		#define NULL	((void *)0)
	#endif
#endif

#define MRDCORP_TO_NONCOPYABLE(class_name)	\
	private:	\
		class_name(const class_name &);	\
		class_name & operator = (const class_name &)

#define MRDCORP_NOT_USED(x)		((void)(x))

#ifndef MRDCORP_DLLAPI
	#ifdef _USRDLL
		#define MRDCORP_DLLAPI		__declspec(dllexport)
	#else // _USRDLL
		#define MRDCORP_DLLAPI		__declspec(dllimport)
	#endif // _USRDLL
#endif // MRDCORP_DLLAPI

#endif // __MRDCORP_MrdCorpDef_H__
