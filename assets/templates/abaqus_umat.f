      SUBROUTINE UMAT(STRESS,STATEV,DDSDDE,SSE,SPD,SCD,
     1 RPL,DDSDDT,DRPLDE,DRPLDT,
     2 STRAN,DSTRAN,TIME,DTIME,TEMP,DTEMP,PREDEF,DPRED,CMNAME,
     3 NDI,NSHR,NTENS,NSTATV,PROPS,NPROPS,COORDS,DROT,PNEWDT,
     4 CELENT,DFGRD0,DFGRD1,NOEL,NPT,LAYER,KSPT,KSTEP,KINC)
C
      INCLUDE 'ABA_PARAM.INC'
C
      CHARACTER*80 CMNAME
      DIMENSION STRESS(NTENS),STATEV(NSTATV),
     1 DDSDDE(NTENS,NTENS),DDSDDT(NTENS),DRPLDE(NTENS),
     2 STRAN(NTENS),DSTRAN(NTENS),TIME(2),PREDEF(1),DPRED(1),
     3 PROPS(NPROPS),COORDS(3),DROT(3,3),DFGRD0(3,3),DFGRD1(3,3)
C
C     ELASTIC CONSTANTS FOR {{material_name}}
C     Crystal Type: {{crystal_type}}
C
      PARAMETER (ZERO=0.D0, ONE=1.D0)
C
C     INITIALIZE J ACOBIAN MATRIX
      DO I=1,NTENS
        DO J=1,NTENS
          DDSDDE(I,J) = ZERO
        ENDDO
      ENDDO
C
C     DEFINE ELASTIC STIFFNESS MATRIX (Cij)
C     Note: ABAQUS uses 1,2,3 for normal and 4,5,6 for shear directions.
C     Standard 11, 22, 33, 12, 13, 23 ordering often maps to 1, 2, 3, 4, 5, 6
C     BUT check specific element formulation. Typically for 3D solid:
C     1=xx, 2=yy, 3=zz, 4=xy, 5=xz, 6=yz (shear engineering strain)
C
      DDSDDE(1,1) = {{C11}}
      DDSDDE(1,2) = {{C12}}
      DDSDDE(1,3) = {{C13}}
      DDSDDE(1,4) = {{C16}}
      DDSDDE(1,5) = {{C15}}
      DDSDDE(1,6) = {{C14}}

      DDSDDE(2,1) = {{C21}}
      DDSDDE(2,2) = {{C22}}
      DDSDDE(2,3) = {{C23}}
      DDSDDE(2,4) = {{C26}}
      DDSDDE(2,5) = {{C25}}
      DDSDDE(2,6) = {{C24}}

      DDSDDE(3,1) = {{C31}}
      DDSDDE(3,2) = {{C32}}
      DDSDDE(3,3) = {{C33}}
      DDSDDE(3,4) = {{C36}}
      DDSDDE(3,5) = {{C35}}
      DDSDDE(3,6) = {{C34}}

      DDSDDE(4,1) = {{C61}}
      DDSDDE(4,2) = {{C62}}
      DDSDDE(4,3) = {{C63}}
      DDSDDE(4,4) = {{C66}}
      DDSDDE(4,5) = {{C65}}
      DDSDDE(4,6) = {{C64}}

      DDSDDE(5,1) = {{C51}}
      DDSDDE(5,2) = {{C52}}
      DDSDDE(5,3) = {{C53}}
      DDSDDE(5,4) = {{C56}}
      DDSDDE(5,5) = {{C55}}
      DDSDDE(5,6) = {{C54}}

      DDSDDE(6,1) = {{C41}}
      DDSDDE(6,2) = {{C42}}
      DDSDDE(6,3) = {{C43}}
      DDSDDE(6,4) = {{C46}}
      DDSDDE(6,5) = {{C45}}
      DDSDDE(6,6) = {{C44}}
C
C     UPDATE STRESS
      DO I=1,NTENS
        DO J=1,NTENS
          STRESS(I) = STRESS(I) + DDSDDE(I,J)*DSTRAN(J)
        ENDDO
      ENDDO
C
      RETURN
      END
