package com.example.sesac.hospital.db.entity;

import com.example.sesac.hospital.dto.HospitalDepartmentDto;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@NoArgsConstructor
@Getter
public class HospitalDepartment {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long departmentId;

    @ManyToOne
    @JoinColumn(name = "hospital_id", insertable = false, updatable = false)
    private Hospital hospital;

    private String hospitalMiddle;
    private String hospitalMajor;

    public static HospitalDepartmentDto toDto(HospitalDepartment hospitalDepartment) {
        return HospitalDepartmentDto.builder()
                .hospitalId(hospitalDepartment.hospital.getHospitalId())
                .departmentId(hospitalDepartment.getDepartmentId())
                .hospitalMajor(hospitalDepartment.getHospitalMajor())
                .hospitalMiddle(hospitalDepartment.getHospitalMiddle())
                .build();
    }
}




