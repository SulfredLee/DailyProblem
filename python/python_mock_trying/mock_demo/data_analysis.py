from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# assume similar classes for Data2 and Data3
class Data1(Base):
    __tablename__ = 'some_table'
    pk1 = Column(Integer, primary_key=True)
    data_val1 = Column(Integer)
    data_val2 = Column(Integer)
    data_val3 = Column(Integer)
    def __init__(self, pk1, val1, val2, val3):
        self.pk1 = pk1
        self.data_val1 = val1
        self.data_val2 = val2
        self.data_val3 = val3

class Data2(Base):
    __tablename__ = 'some_table_003'
    pk1 = Column(Integer, primary_key=True)
    data_val1 = Column(Integer)
    data_val2 = Column(Integer)
    data_val3 = Column(Integer)
    def __init__(self, pk1, val1, val2, val3):
        self.pk1 = pk1
        self.data_val1 = val1
        self.data_val2 = val2
        self.data_val3 = val3

class Data3(Base):
    __tablename__ = 'some_table_004'
    pk1 = Column(Integer, primary_key=True)
    data_val1 = Column(Integer)
    data_val2 = Column(Integer)
    data_val3 = Column(Integer)
    def __init__(self, pk1, val1, val2, val3):
        self.pk1 = pk1
        self.data_val1 = val1
        self.data_val2 = val2
        self.data_val3 = val3

class CombinedAnalysis(Base):
    __tablename__ = 'some_table_002'
    pk1 = Column(Integer, primary_key=True)
    analysis_val1 = Column(Integer)
    analysis_val2 = Column(Integer)
    analysis_val3 = Column(Integer)
    def __init__(self, pk1, val1, val2, val3):
        self.pk1 = pk1
        self.analysis_val1 = val1
        self.analysis_val2 = val2
        self.analysis_val3 = val3

    def __eq__(self, other):
        if not isinstance(other, CombinedAnalysis):
            return NotImplemented
        return (
            self.analysis_val1 == other.analysis_val1
            and self.analysis_val2 == other.analysis_val2
            and self.analysis_val3 == other.analysis_val3
        )

def analysis(dataset_first, dataset_second):
    return dataset_first

def intergrate_analysis(d_1, d_2, d_3):
    return d_1

def complex_data_analysis(cfg, session):
    # collects some data upto some point
    dataset1 = session.query(Data1).filter(Data1.data_val1 < 20)
    dataset2 = session.query(Data2).filter(Data2.data_val2 < 30)
    dataset3 = session.query(Data3).filter(Data3.data_val3 < 40)
    # performs some analysis
    analysis12 = analysis(dataset1, dataset2)
    analysis13 = analysis(dataset1, dataset3)
    analysis23 = analysis(dataset2, dataset3)
    # combine the data analysis (returns object CombinedAnalysis)
    combined_analysis = intergrate_analysis(analysis12, analysis13, analysis23)
    # assume the combined_analysis are stored in some SQL table
    session.add_all(combined_analysis)
    session.commit()
