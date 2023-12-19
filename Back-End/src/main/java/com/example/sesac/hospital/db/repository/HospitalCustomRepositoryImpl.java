package com.example.sesac.hospital.db.repository;

import com.example.sesac.hospital.dto.HospitalDepReq;
import com.example.sesac.hospital.dto.HospitalReviewSumDto;
import com.querydsl.core.types.Projections;
import com.querydsl.core.types.dsl.BooleanExpression;
import com.querydsl.jpa.impl.JPAQueryFactory;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;
import org.springframework.util.StringUtils;

import java.util.List;

import static com.example.sesac.hospital.db.entity.QHospital.hospital;
import static com.example.sesac.hospital.db.entity.QHospitalDepartment.hospitalDepartment;
import static com.example.sesac.review.db.entity.QReviewSum.reviewSum;


@Repository
@RequiredArgsConstructor
public class HospitalCustomRepositoryImpl implements HospitalCustomRepository {
    private final JPAQueryFactory query;

    @Override
    public List<HospitalReviewSumDto> getHospital(HospitalDepReq hospitalDepReq) {
        return query.select(Projections.constructor(HospitalReviewSumDto.class, hospital.hospitalId, hospital.hospitalName, reviewSum.positiveReviewCnt, reviewSum.negativeReviewCnt,
                        reviewSum.positivePercentage, reviewSum.negativePercentage, reviewSum.reviewTotalCnt))
                .from(hospital)
                .leftJoin(hospitalDepartment).on(hospital.hospitalId.eq(hospitalDepartment.hospital.hospitalId))
                .leftJoin(reviewSum).on(hospital.hospitalId.eq(reviewSum.hospital.hospitalId))
                .where(whereCondition(hospitalDepReq))
//                .where(hospitalDepartment.hospitalMiddle.eq(hospitalDepReq.getDepartment()).and(hospital.hospitalAddress.like("%" + hospitalDepReq.getLocation() + "%")))
                .orderBy(reviewSum.reviewTotalCnt.desc())
                .fetch();
    }

    private BooleanExpression whereCondition(HospitalDepReq hospitalDepReq){
        BooleanExpression booleanExpression = null;
        booleanExpression = eqLocation(booleanExpression, hospitalDepReq.getLocation());
        booleanExpression = eqDepartment(booleanExpression, hospitalDepReq.getDepartment());
        return booleanExpression;
    }

    private BooleanExpression eqDepartment(BooleanExpression be, String department) {
        BooleanExpression eq = null;
        if (StringUtils.hasText(department)) {
            eq = hospitalDepartment.hospitalMiddle.eq(department);
        }
        if (be == null)
            return eq;
        if (eq == null)
            return be;
        return be.and(eq);
    }

    private BooleanExpression eqLocation(BooleanExpression be, String location) {
        BooleanExpression eq = null;
        if (StringUtils.hasText(location)) {
            eq = hospital.hospitalAddress.like("%" + location + "%");
        }

        if (be == null)
            return eq;

        if (eq == null)
            return be;

        return be.and(eq);
    }
}
