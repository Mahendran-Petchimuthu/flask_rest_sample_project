from db.base import db

field_mapping = {
                 'product_id':'productId',
                 'name':'name',
                 'description':'description',
                 'jwt_secret':'jwtSecret',
                 'encryption_key':'encryptionKey',
                 'is_active':'isActive',
                 'create_time':'createTime',
                 'modify_time':'modifyTime'
                }
                
class ProductModel(db.Model):
    """
    Product details (API client), using which system APIs can be accessed
    """

    __tablename__ = 'products'

    product_id = db.Column(db.BigInteger, primary_key=True, doc="Product Id")
    name = db.Column(db.Text, nullable=False, doc="Product Name")
    description = db.Column(db.Text, nullable=True, doc="Short description about product")
    jwt_secret = db.Column(db.Text, nullable=False, doc="Key to validate jwt token")
    encryption_key = db.Column(db.Text, nullable=False, doc="Key to encrypt/decrypt data source credentials")
    is_active = db.Column(db.Boolean, nullable=False,default=False, doc="To indicate product is active or not")  
    create_time = db.Column(db.BigInteger, nullable=False, doc="Created timestamp")
    modify_time = db.Column(db.BigInteger, nullable=False, doc="Last modified timestamp")
    #accounts = db.relationship("Account", backref="product")

    def __init__(self, productId, name, description, jwtSecret, encryptionKey, isActive, createTime, modifyTime):
        self.product_id = productId
        self.name = name
        self.description = description
        self.jwt_secret = jwtSecret
        self.encryption_key = encryptionKey
        self.is_active = isActive
        self.create_time = createTime
        self.modify_time = modifyTime

    def json(self):
        #return {'name': self.name, 'accounts': [account.json() for account in self.accounts.all()]}
        data = {}
        product_object = self.__dict__
        for k, v in field_mapping.items():
            data[v] = product_object.get(k)

        return data

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(product_id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()