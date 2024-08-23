from config.conexao import engine, Base
from sqlalchemy import Column, Integer, String


class Usuarios(Base):
    __tablename__ = "usuarios"
    cpf = Column(String(11), primary_key=True, autoincrement=False)
    nome = Column(String(70), nullable=False)
    telefone = Column(String(12), nullable=False)
    endereco = Column(String(200), nullable=False)

    def as_dict(self):
        return {
            "cpf": self.cpf,
            "nome": self.nome,
            "telefone": self.telefone,
            "endereco": self.endereco
        }


Base.metadata.create_all(engine)
