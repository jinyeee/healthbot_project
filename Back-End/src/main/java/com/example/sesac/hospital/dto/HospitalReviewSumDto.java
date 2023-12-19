package com.example.sesac.hospital.dto;

import com.querydsl.core.annotations.QueryProjection;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@NoArgsConstructor
public class HospitalReviewSumDto {
    private Long hospitalId;
    private String hospitalName;
    private Long positiveReviewCnt;
    private Long negativeReviewCnt;
    private Double positivePercentage;
    private Double negativePercentage;
    private Long reviewTotalCnt;

    @QueryProjection
    public HospitalReviewSumDto(Long hospitalId, String hospitalName, Long positiveReviewCnt, Long negativeReviewCnt, Double positivePercentage, Double negativePercentage, Long reviewTotalCnt) {
        this.hospitalId = hospitalId;
        this.hospitalName = hospitalName;
        this.positiveReviewCnt = positiveReviewCnt;
        this.negativeReviewCnt = negativeReviewCnt;
        this.positivePercentage = positivePercentage;
        this.negativePercentage = negativePercentage;
        this.reviewTotalCnt = reviewTotalCnt;
    }
}