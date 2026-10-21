INSERT INTO finser_banks_db.output_simulatori_clean (
    id_outx,
    fetching_date,
    id_input,
    rata_mensile,
    entity,
    purpose,

    total_amount,
    monthly_repay_min,
    monthly_repay_max,
    monthly_no_ins,
    monthly_yes_ins,
    prelim_fees_min,
    prelim_fees_max,
    prelim_fees_value,
    service_fee_min,
    service_fee_max,
    service_fee_value,
    collect_charge_min,
    collect_charge_max,
    collect_charge_value,
    due_amount_min,
    due_amount_max,
    due_amount_no_ins,
    due_amount_yes_ins,
    insurance_value,

    tan_range_min,
    tan_range_max,
    taeg_range_min,
    taeg_range_max,
    tan_value_no_ins,
    tan_value_yes_ins,
    taeg_value_no_ins,
    taeg_value_yes_ins,
    tan_min_physical,
    tan_max_physical,
    taeg_min_physical,
    taeg_max_physical,
    tan_physical_value,
    taeg_physical_value,

    duration_min,
    duration_max,
    duration_value
)
SELECT
    id_outx,

    -- 日期
    CASE
        WHEN fetching_date IS NULL OR TRIM(fetching_date) = '' THEN NULL
        WHEN TRIM(fetching_date) NOT REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' THEN NULL
        ELSE CAST(TRIM(fetching_date) AS DATE)
    END,

    -- id_input (int)
    CASE
        WHEN id_input IS NULL OR TRIM(id_input) = '' THEN NULL
        WHEN TRIM(id_input) NOT REGEXP '^-?[0-9]+$' THEN NULL
        ELSE CAST(TRIM(id_input) AS SIGNED)
    END,

    rata_mensile,

    NULLIF(TRIM(TS00), ''),
    NULLIF(TRIM(TS02), ''),

    ------------------------------------------------------------------
    -- 金额类：双重替换 + 正则保护 → DECIMAL(15,2)
    ------------------------------------------------------------------
    CASE
        WHEN TS01 IS NULL OR TRIM(TS01) = '' THEN NULL
        WHEN REPLACE(REPLACE(TRIM(TS01),'.',''),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(REPLACE(TRIM(TS01),'.',''),',','.') AS DECIMAL(15,2))
    END,
    CASE
        WHEN TS11 IS NULL OR TRIM(TS11) = '' THEN NULL
        WHEN REPLACE(REPLACE(TRIM(TS11),'.',''),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(REPLACE(TRIM(TS11),'.',''),',','.') AS DECIMAL(15,2))
    END,
    CASE
        WHEN TS12 IS NULL OR TRIM(TS12) = '' THEN NULL
        WHEN REPLACE(REPLACE(TRIM(TS12),'.',''),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(REPLACE(TRIM(TS12),'.',''),',','.') AS DECIMAL(15,2))
    END,
    CASE
        WHEN TS13 IS NULL OR TRIM(TS13) = '' THEN NULL
        WHEN REPLACE(REPLACE(TRIM(TS13),'.',''),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(REPLACE(TRIM(TS13),'.',''),',','.') AS DECIMAL(15,2))
    END,
    CASE
        WHEN TS14 IS NULL OR TRIM(TS14) = '' THEN NULL
        WHEN REPLACE(REPLACE(TRIM(TS14),'.',''),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(REPLACE(TRIM(TS14),'.',''),',','.') AS DECIMAL(15,2))
    END,
    CASE
        WHEN TS18 IS NULL OR TRIM(TS18) = '' THEN NULL
        WHEN REPLACE(REPLACE(TRIM(TS18),'.',''),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(REPLACE(TRIM(TS18),'.',''),',','.') AS DECIMAL(15,2))
    END,
    CASE
        WHEN TS19 IS NULL OR TRIM(TS19) = '' THEN NULL
        WHEN REPLACE(REPLACE(TRIM(TS19),'.',''),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(REPLACE(TRIM(TS19),'.',''),',','.') AS DECIMAL(15,2))
    END,
    CASE
        WHEN TS20 IS NULL OR TRIM(TS20) = '' THEN NULL
        WHEN REPLACE(REPLACE(TRIM(TS20),'.',''),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(REPLACE(TRIM(TS20),'.',''),',','.') AS DECIMAL(15,2))
    END,
    CASE
        WHEN TS21 IS NULL OR TRIM(TS21) = '' THEN NULL
        WHEN REPLACE(REPLACE(TRIM(TS21),'.',''),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(REPLACE(TRIM(TS21),'.',''),',','.') AS DECIMAL(15,2))
    END,
    CASE
        WHEN TS22 IS NULL OR TRIM(TS22) = '' THEN NULL
        WHEN REPLACE(REPLACE(TRIM(TS22),'.',''),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(REPLACE(TRIM(TS22),'.',''),',','.') AS DECIMAL(15,2))
    END,
    CASE
        WHEN TS23 IS NULL OR TRIM(TS23) = '' THEN NULL
        WHEN REPLACE(REPLACE(TRIM(TS23),'.',''),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(REPLACE(TRIM(TS23),'.',''),',','.') AS DECIMAL(15,2))
    END,
    CASE
        WHEN TS24 IS NULL OR TRIM(TS24) = '' THEN NULL
        WHEN REPLACE(REPLACE(TRIM(TS24),'.',''),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(REPLACE(TRIM(TS24),'.',''),',','.') AS DECIMAL(15,2))
    END,
    CASE
        WHEN TS25 IS NULL OR TRIM(TS25) = '' THEN NULL
        WHEN REPLACE(REPLACE(TRIM(TS25),'.',''),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(REPLACE(TRIM(TS25),'.',''),',','.') AS DECIMAL(15,2))
    END,
    CASE
        WHEN TS26 IS NULL OR TRIM(TS26) = '' THEN NULL
        WHEN REPLACE(REPLACE(TRIM(TS26),'.',''),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(REPLACE(TRIM(TS26),'.',''),',','.') AS DECIMAL(15,2))
    END,
    CASE
        WHEN TS33 IS NULL OR TRIM(TS33) = '' THEN NULL
        WHEN REPLACE(REPLACE(TRIM(TS33),'.',''),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(REPLACE(TRIM(TS33),'.',''),',','.') AS DECIMAL(15,2))
    END,
    CASE
        WHEN TS34 IS NULL OR TRIM(TS34) = '' THEN NULL
        WHEN REPLACE(REPLACE(TRIM(TS34),'.',''),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(REPLACE(TRIM(TS34),'.',''),',','.') AS DECIMAL(15,2))
    END,
    CASE
        WHEN TS35 IS NULL OR TRIM(TS35) = '' THEN NULL
        WHEN REPLACE(REPLACE(TRIM(TS35),'.',''),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(REPLACE(TRIM(TS35),'.',''),',','.') AS DECIMAL(15,2))
    END,
    CASE
        WHEN TS36 IS NULL OR TRIM(TS36) = '' THEN NULL
        WHEN REPLACE(REPLACE(TRIM(TS36),'.',''),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(REPLACE(TRIM(TS36),'.',''),',','.') AS DECIMAL(15,2))
    END,
    CASE
        WHEN TS37 IS NULL OR TRIM(TS37) = '' THEN NULL
        WHEN REPLACE(REPLACE(TRIM(TS37),'.',''),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(REPLACE(TRIM(TS37),'.',''),',','.') AS DECIMAL(15,2))
    END,

    ------------------------------------------------------------------
    -- 利率类：单替换 + 正则保护 → DECIMAL(6,3)
    ------------------------------------------------------------------
    CASE
        WHEN TS03 IS NULL OR TRIM(TS03) = '' THEN NULL
        WHEN REPLACE(TRIM(TS03),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(TRIM(TS03),',','.') AS DECIMAL(6,3))
    END,
    CASE
        WHEN TS04 IS NULL OR TRIM(TS04) = '' THEN NULL
        WHEN REPLACE(TRIM(TS04),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(TRIM(TS04),',','.') AS DECIMAL(6,3))
    END,
    CASE
        WHEN TS05 IS NULL OR TRIM(TS05) = '' THEN NULL
        WHEN REPLACE(TRIM(TS05),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(TRIM(TS05),',','.') AS DECIMAL(6,3))
    END,
    CASE
        WHEN TS06 IS NULL OR TRIM(TS06) = '' THEN NULL
        WHEN REPLACE(TRIM(TS06),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(TRIM(TS06),',','.') AS DECIMAL(6,3))
    END,
    CASE
        WHEN TS07 IS NULL OR TRIM(TS07) = '' THEN NULL
        WHEN REPLACE(TRIM(TS07),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(TRIM(TS07),',','.') AS DECIMAL(6,3))
    END,
    CASE
        WHEN TS08 IS NULL OR TRIM(TS08) = '' THEN NULL
        WHEN REPLACE(TRIM(TS08),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(TRIM(TS08),',','.') AS DECIMAL(6,3))
    END,
    CASE
        WHEN TS09 IS NULL OR TRIM(TS09) = '' THEN NULL
        WHEN REPLACE(TRIM(TS09),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(TRIM(TS09),',','.') AS DECIMAL(6,3))
    END,
    CASE
        WHEN TS10 IS NULL OR TRIM(TS10) = '' THEN NULL
        WHEN REPLACE(TRIM(TS10),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(TRIM(TS10),',','.') AS DECIMAL(6,3))
    END,
    CASE
        WHEN TS27 IS NULL OR TRIM(TS27) = '' THEN NULL
        WHEN REPLACE(TRIM(TS27),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(TRIM(TS27),',','.') AS DECIMAL(6,3))
    END,
    CASE
        WHEN TS28 IS NULL OR TRIM(TS28) = '' THEN NULL
        WHEN REPLACE(TRIM(TS28),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(TRIM(TS28),',','.') AS DECIMAL(6,3))
    END,
    CASE
        WHEN TS29 IS NULL OR TRIM(TS29) = '' THEN NULL
        WHEN REPLACE(TRIM(TS29),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(TRIM(TS29),',','.') AS DECIMAL(6,3))
    END,
    CASE
        WHEN TS30 IS NULL OR TRIM(TS30) = '' THEN NULL
        WHEN REPLACE(TRIM(TS30),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(TRIM(TS30),',','.') AS DECIMAL(6,3))
    END,
    CASE
        WHEN TS31 IS NULL OR TRIM(TS31) = '' THEN NULL
        WHEN REPLACE(TRIM(TS31),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(TRIM(TS31),',','.') AS DECIMAL(6,3))
    END,
    CASE
        WHEN TS32 IS NULL OR TRIM(TS32) = '' THEN NULL
        WHEN REPLACE(TRIM(TS32),',','.') NOT REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN NULL
        ELSE CAST(REPLACE(TRIM(TS32),',','.') AS DECIMAL(6,3))
    END,

    ------------------------------------------------------------------
    -- 期限类：INT
    ------------------------------------------------------------------
    CASE
        WHEN TS15 IS NULL OR TRIM(TS15) = '' THEN NULL
        WHEN TRIM(TS15) NOT REGEXP '^-?[0-9]+$' THEN NULL
        ELSE CAST(TRIM(TS15) AS SIGNED)
    END,
    CASE
        WHEN TS16 IS NULL OR TRIM(TS16) = '' THEN NULL
        WHEN TRIM(TS16) NOT REGEXP '^-?[0-9]+$' THEN NULL
        ELSE CAST(TRIM(TS16) AS SIGNED)
    END,
    CASE
        WHEN TS17 IS NULL OR TRIM(TS17) = '' THEN NULL
        WHEN TRIM(TS17) NOT REGEXP '^-?[0-9]+$' THEN NULL
        ELSE CAST(TRIM(TS17) AS SIGNED)
    END

FROM finser_banks_db.output_simulatori
WHERE fetching_date BETWEEN '2026-10-12' AND '2026-10-13';