package com.example.sesac.review.db.entity;

import com.example.sesac.hospital.db.entity.Hospital;
import com.example.sesac.review.dto.HospitalReviewDto;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Getter
@NoArgsConstructor
public class HospitalReview {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long reviewId;

    @ManyToOne
    @JoinColumn(name = "hospital_id", insertable = false, updatable = false)
    private Hospital hospital;
    private String content;


    public static HospitalReviewDto toDto(HospitalReview hospitalReview) {
        return HospitalReviewDto.builder()
                .reviewId(hospitalReview.reviewId)
                .hospitalName(hospitalReview.hospital.getHospitalName())
                .content(hospitalReview.content)
                .build();
    }


}
