from sqlalchemy import create_engine

DB_URL = 'postgresql://xflrotuhigtqrv:7ce85844eb725ce394364f3f08bc1948fc5c60056fd51083d78a0d054cb05231@ec2-52-1-20-236.compute-1.amazonaws.com:5432/df52anouucpo1v'
engine = create_engine(DB_URL, echo=False)
