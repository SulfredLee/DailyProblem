INSERT INTO hk.company
    (id, name, start_up_time, owner)
    VALUES ('cjisldfh28fgsvKL9', 'OO Capital', '2022-01-01 08:30:00', '{Mr A, Miss A}')
    , ('cjieddfh28fgsvKL9', 'PP Capital', '2022-01-02 08:30:00', '{Mr A, Miss B}')
    ON CONFLICT (id)
    DO NOTHING;

INSERT INTO hk.department
    (id, name, start_time, end_time, address, company_id)
  VALUES ('sdfauvbmw83hfs90df', 'Software Dev', '09:00:00', '18:00:00', '2/F', 'cjieddfh28fgsvKL9')
    , ('sdfauvbmw93hfs90df', 'Trading', '09:00:00', '18:00:00', '3/F', 'cjieddfh28fgsvKL9')
    , ('sdfauvamw93hfs90df', 'HR', '09:00:00', '18:00:00', '4/F', 'cjieddfh28fgsvKL9')
    , ('sdfaudbmw93hfs90df', 'Management', '09:00:00', '18:00:00', '5/F', 'cjieddfh28fgsvKL9')
    , ('sdfeuvbmw83hfs90df', 'Software Dev', '09:00:00', '18:00:00', '2/F', 'cjisldfh28fgsvKL9')
    , ('swfauvbmw93hfs90df', 'Trading', '09:00:00', '18:00:00', '3/F', 'cjisldfh28fgsvKL9')
    , ('sdfauvamw93hhs90df', 'HR', '09:00:00', '18:00:00', '4/F', 'cjisldfh28fgsvKL9')
    , ('sdfauqbmw93hfs90df', 'Management', '09:00:00', '18:00:00', '5/F', 'cjisldfh28fgsvKL9')
    ON CONFLICT (id)
    DO NOTHING;

INSERT INTO hk.employee
    (id, name, gender, is_full_time, join_time, department_id)
    VALUES ('piruewjvbs324hg', 'Mr A', 'M', true, '2022-01-01 06:30:00', 'sdfaudbmw93hfs90df')
    , ('piruewjvbw324hg', 'Miss A', 'F', true, '2022-01-01 06:30:00', 'sdfaudbmw93hfs90df')
    , ('piruewjvbs3243g', 'Potato A', 'M', true, '2022-01-01 06:30:00', 'sdfauvbmw83hfs90df')
    , ('pirwewjvbs3243g', 'Potato B', 'F', true, '2022-01-01 06:30:00', 'sdfauvbmw83hfs90df')
    , ('piruewjvbw324rg', 'Miss A', 'F', true, '2022-01-01 06:30:00', 'sdfaudbmw93hfs90df')
    , ('pirsewjvbs324hg', 'Mr A', 'M', true, '2022-01-01 06:30:00', 'sdfauqbmw93hfs90df')
    , ('pieuewjvbw324hg', 'Miss B', 'F', true, '2022-01-01 06:30:00', 'sdfauqbmw93hfs90df')
    , ('pwruewjvbs3243g', 'Potato A', 'M', true, '2022-01-01 06:30:00', 'sdfauvamw93hhs90df')
    , ('pirwekjvbs3243g', 'Potato B', 'F', true, '2022-01-01 06:30:00', 'sdfauvamw93hhs90df')
    ON CONFLICT (id)
    DO NOTHING;
