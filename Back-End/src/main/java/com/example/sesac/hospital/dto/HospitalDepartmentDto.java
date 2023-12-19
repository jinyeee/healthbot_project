package com.example.sesac.hospital.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
public class HospitalDepartmentDto {
    private Long departmentId;
    private Long hospitalId;
    private String hospitalMiddle;
    private String hospitalMajor;


    @Builder
    public HospitalDepartmentDto(Long departmentId, Long hospitalId, String hospitalMiddle, String hospitalMajor) {
        this.departmentId = departmentId;
        this.hospitalId = hospitalId;
        this.hospitalMiddle = hospitalMiddle;
        this.hospitalMajor = hospitalMajor;
    }
}
