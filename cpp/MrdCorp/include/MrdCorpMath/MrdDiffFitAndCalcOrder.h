//////////////////////////////////////////////////////////////////////////
// LiYun, 2014 - 2014
//////////////////////////////////////////////////////////////////////////

#ifndef __MRDCORP_MrdDiffFitAndCalcOrder_H__
#define __MRDCORP_MrdDiffFitAndCalcOrder_H__

#include <MrdCorpMath/MrdDef_CorpMath.h>

#define MRDCORPMATH_FIT_AND_ORDER__MAX_ORDER		10
#define MRDCORPMATH_FIT_AND_ORDER__MAX_M			5

#ifdef __cplusplus
extern "C" {
#endif // __cplusplus

	//////////////////////////////////////////////////////////////////////////
	// 纯C接口
	typedef struct _t_MrdCorpMath_DiffFit_Beta
	{
		double arrF3[MRDCORPMATH_FIT_AND_ORDER__MAX_M + 3];
		double arrF2[MRDCORPMATH_FIT_AND_ORDER__MAX_M + 2];
		double arrF1[MRDCORPMATH_FIT_AND_ORDER__MAX_M + 1];
	} MrdCorpMath_DiffFit_Beta;
	typedef struct _t_MrdCorpMath_DiffFit_Result
	{
		int iOrder; // 返回负数表示计算过程中出错了
		int iFulfillStep; // 0：计算公式3时已经满足条件，1：计算公式2时已经满足条件，2：计算公式1时已经满足条件
		MrdCorpMath_DiffFit_Beta arrBeta[MRDCORPMATH_FIT_AND_ORDER__MAX_ORDER + 1];
	} MrdCorpMath_DiffFit_Result;

	typedef struct _cc_MrdCorpMath_CalcDiffOrder*		MrdCorpMath_CalcDiffOrder_Handle;
	//typedef unsigned int		MrdCorpMath_CalcDiffOrder_Handle;
	// 创建/销毁 对象
	MRDCORPMATH_DLLAPI MrdCorpMath_CalcDiffOrder_Handle MRDCORPMATH_API mrdCorpMath_CalcDiffOrder_create(void);
	MRDCORPMATH_DLLAPI void MRDCORPMATH_API mrdCorpMath_CalcDiffOrder_destroy(MrdCorpMath_CalcDiffOrder_Handle hCalc);
	//
	// 设定参数
	MRDCORPMATH_DLLAPI size_t MRDCORPMATH_API mrdCorpMath_CalcDiffOrder__get_m(MrdCorpMath_CalcDiffOrder_Handle hCalc);
	MRDCORPMATH_DLLAPI void MRDCORPMATH_API mrdCorpMath_CalcDiffOrder__set_m(MrdCorpMath_CalcDiffOrder_Handle hCalc, size_t szM);
	//
	MRDCORPMATH_DLLAPI size_t MRDCORPMATH_API mrdCorpMath_CalcDiffOrder__get_max_iteration(MrdCorpMath_CalcDiffOrder_Handle hCalc);
	MRDCORPMATH_DLLAPI void MRDCORPMATH_API mrdCorpMath_CalcDiffOrder__set_max_iteration(MrdCorpMath_CalcDiffOrder_Handle hCalc, size_t szMaxIterNum);
	//
	MRDCORPMATH_DLLAPI double MRDCORPMATH_API mrdCorpMath_CalcDiffOrder__get_lower_delta_0(MrdCorpMath_CalcDiffOrder_Handle hCalc);
	MRDCORPMATH_DLLAPI void MRDCORPMATH_API mrdCorpMath_CalcDiffOrder__set_lower_delta_0(MrdCorpMath_CalcDiffOrder_Handle hCalc, double dblLowerDelta_0);
	//
	MRDCORPMATH_DLLAPI double MRDCORPMATH_API mrdCorpMath_CalcDiffOrder__get_threshold_1(MrdCorpMath_CalcDiffOrder_Handle hCalc);
	MRDCORPMATH_DLLAPI void MRDCORPMATH_API mrdCorpMath_CalcDiffOrder__set_threshold_1(MrdCorpMath_CalcDiffOrder_Handle hCalc, double dblThreshold);
	MRDCORPMATH_DLLAPI double MRDCORPMATH_API mrdCorpMath_CalcDiffOrder__get_threshold_2(MrdCorpMath_CalcDiffOrder_Handle hCalc);
	MRDCORPMATH_DLLAPI void MRDCORPMATH_API mrdCorpMath_CalcDiffOrder__set_threshold_2(MrdCorpMath_CalcDiffOrder_Handle hCalc, double dblThreshold);
	MRDCORPMATH_DLLAPI double MRDCORPMATH_API mrdCorpMath_CalcDiffOrder__get_threshold_3(MrdCorpMath_CalcDiffOrder_Handle hCalc);
	MRDCORPMATH_DLLAPI void MRDCORPMATH_API mrdCorpMath_CalcDiffOrder__set_threshold_3(MrdCorpMath_CalcDiffOrder_Handle hCalc, double dblThreshold);
	//
	// 计算
	MRDCORPMATH_DLLAPI void MRDCORPMATH_API mrdCorpMath_CalcDiffOrder__do_calc(MrdCorpMath_CalcDiffOrder_Handle hCalc
		, MrdCorpMath_DiffFit_Result& rResult
		, const double* pcSample, size_t szCntSample);
	//////////////////////////////////////////////////////////////////////////

#ifdef __cplusplus
} // end of extern "C"
#endif // __cplusplus

#ifdef __cplusplus
namespace mrdlab
{

	//////////////////////////////////////////////////////////////////////////
	// C++ 接口
	class MrdCorpMath_CalcDiffOrder_Impl;
	//
	class MRDCORPMATH_DLLAPI MrdCorpMath_CalcDiffOrder
	{
	public:
		MrdCorpMath_CalcDiffOrder(void);
		~MrdCorpMath_CalcDiffOrder(void);
		// 计算参数
		// m，默认：2
		size_t get_m(void) const;
		void set_m(size_t szM);
		// 最大迭代次数，默认：32
		size_t get_max_iteration(void) const;
		void set_max_iteration(size_t szMaxIterNum);
		// lower_delta_0
		double get_lower_delta_0(void) const;
		void set_lower_delta_0(double dblLowerDelta_0);
		// 分别对应公式F1到F3的阈值
		// 默认值分别为：-1.95, -2.86, -3.41
		double get_threshold_1(void) const;
		void set_threshold_1(double dblThreshold);
		double get_threshold_2(void) const;
		void set_threshold_2(double dblThreshold);
		double get_threshold_3(void) const;
		void set_threshold_3(double dblThreshold);
		//
		// rResult：计算输出结果
		// pcSample：样本数据，szCntSample：样本数量
		void do_calc(MrdCorpMath_DiffFit_Result& rResult, const double* pcSample, size_t szCntSample);

	private:
		MrdCorpMath_CalcDiffOrder_Impl* m_pCalcImpl;
	};
	//////////////////////////////////////////////////////////////////////////

} // namespace mrdlab
#endif // __cplusplus

#endif // __MRDCORP_MrdDiffFitAndCalcOrder_H__
