package com.example.sesac.hospital.db.entity;

import com.example.sesac.hospital.dto.HospitalDto;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@NoArgsConstructor
@Getter
public class Hospital {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long hospitalId;
    private String hospitalName;
    private String hospitalAddress;
    private String hospitalCode;
    private String hospitalPost;
    private String hospitalTell;
    private double hospitalLongitude;
    private double hospitalLatitude;

    @Builder
    public Hospital(String hospitalName, String hospitalAddress
            , String hospitalCode, String hospitalPost, String hospitalTell
            , double hospitalLongitude, double hospitalLatitude) {
        this.hospitalName = hospitalName;
        this.hospitalAddress = hospitalAddress;
        this.hospitalCode = hospitalCode;
        this.hospitalPost = hospitalPost;
        this.hospitalTell = hospitalTell;
        this.hospitalLongitude = hospitalLongitude;
        this.hospitalLatitude = hospitalLatitude;
    }

    public static HospitalDto toDto(Hospital hospital) {
        return HospitalDto.builder()
                .hospitalId(hospital.getHospitalId())
                .hospitalName(hospital.getHospitalName())
                .hospitalAddress(hospital.getHospitalAddress())
                .hospitalCode(hospital.getHospitalCode())
                .hospitalPost(hospital.getHospitalPost())
                .hospitalTell(hospital.getHospitalTell())
                .hospitalLongitude(hospital.getHospitalLongitude())
                .hospitalLatitude(hospital.getHospitalLatitude())
                .build();
    }

    public static Hospital toEntity(HospitalDto hospitalDto) {
        return Hospital.builder()
                .hospitalName(hospitalDto.getHospitalName())
                .hospitalAddress(hospitalDto.getHospitalAddress())
                .hospitalCode(hospitalDto.getHospitalCode())
                .hospitalPost(hospitalDto.getHospitalPost())
                .hospitalTell(hospitalDto.getHospitalTell())
                .hospitalLongitude(hospitalDto.getHospitalLongitude())
                .hospitalLatitude(hospitalDto.getHospitalLatitude())
                .build();
    }
}

