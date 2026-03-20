from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import insert
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine

Base = declarative_base()

class Oplote(Base):
    __tablename__ = "oplote"
    # atributos
    numeracao = Column(Integer, primary_key=True)
    produto = Column(Integer,ForeignKey("produtos.codigoProduto"))
    quantidade = Column(Integer)
    status = Column(String)
    substatus = Column(Integer)
    relationship(Base)

    guiaMovimentacao = relationship("GM", back_populates="ordemProdGM")

    def __repr__(self):
        return (f"oplote(numeracao={self.numeracao}, produto={self.produto}, "
                f"quantidade={self.quantidade}, substatus={self.substatus},status={self.status})")

class GM(Base):
    __tablename__ = "guiamovimentacao"
    numeroof = Column(Integer, ForeignKey("oplote.numeracao"))
    codigoitem= Column(Integer, primary_key=True, nullable=False)
    dataInicio = Column(DateTime)
    dataTermino = Column(DateTime)
    produzido = Column(Integer, nullable=False)
    dataValidade = Column(DateTime)
    lote = Column(String)

    ordemProdGM = relationship("Oplote", back_populates="guiaMovimentacao")

    def __repr__(self):
        return (f"guiamovimentacao(numeroof={self.numeroof}, codigoitem={self.codigoitem}, dataInicio={self.dataInicio}, dataTermino={self.dataTermino}, produzido={self.produzido}, lote={self.lote})")

try:
    #engine = create_engine(f"postgresql+psycopg2://root:123panoramix"f"@177.102.229.85:9000/medsharp")
    engine = create_engine(
        f"mysql+mysqlconnector://root:123panoramix@localhost:3306/medsharp"
    )
    novoRegistroGM = insert(GM).values(
                numeroof=1234567,
                codigoitem=1,
                lote="Stranger Things",
                produzido=100,
                dataInicio="2025-10-31 00:00:00",
                dataTermino="2025-10-31 00:00:00"
            )

    with engine.connect() as conn:
        conn.execute(novoRegistroGM)
        conn.commit()

except Exception as erroConexao:
    print("Não foi possível realizar a conexão")
    print(erroConexao)