# -*- coding: utf-8 -*-
#  Copyright (c) 2021 The Project Cargamos Authors

from app import db, commun

class StockMove(commun.BaseModel):
    
    __tablename__ = "stock_move"

    type = db.Column(db.String(10), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouse.id"), nullable=False)

    def __init__(self, name, type, qty, product_id, warehouse_id):
        self.name = name
        self.type = type
        self.qty = qty
        self.product_id = product_id
        self.warehouse_id = warehouse_id

    def serialize(self):
        return {
            'name': self.name, 
            #'type': self.type, 
            'qty': self.qty,
            'product_id': self.product_id,
            'warehouse_id': self.warehouse_id
        }

    @staticmethod
    def by(**kwargs):
        return StockMove.query.filter_by(**kwargs).first_or_404(description='Record with {} is not available'.format(str(kwargs)))
    
    @staticmethod
    def all():
        return StockMove.query.all()


def next_move(ttype):
    """
        Return stock move name by type.
        format: TYPE/NEXT_NUMBER (e.g SO/1 or PO/1)
    """
    count = db.session.query(StockMove.id).count() + 1
    return str('SO/' if ttype =='sale' else 'PO/') + str(count)

def stock_all():
    return _get_stock()

def stock_product(product_id:int):
    filter = " where product_id=%s " % product_id
    return _get_stock( filter=filter)

def stock_warehouse(warehouse_id:int):
    filter = " where warehouse_id=%s " %  warehouse_id
    return _get_stock( filter=filter)

def stock_product_warehouse(product_id:int, warehouse_id:int):
    filter = " where product_id=%s and warehouse_id=%s " % (product_id, warehouse_id)
    return _get_stock( filter=filter)


def _get_stock(filter=""):

    query="""
        SELECT 
            T3.qty, 
            T3.product_id,            
            product.name product_name, 
            T3.warehouse_id,
            warehouse.name warehouse_name
        FROM( 
            SELECT 
                sum(T2.qty) qty, 
                T2.product_id, 
                T2.warehouse_id 
            FROM (
                SELECT 
                    T1.type, 
                    CASE WHEN T1.type = 'out' THEN T1.qty *-1
                    ELSE T1.qty END AS qty, 
                    T1.product_id, T1.warehouse_id 
                from  (
                    select 
                        type, sum(qty) qty,
                        product_id, warehouse_id
                    from stock_move %s
                    GROUP by type, product_id, warehouse_id
                )T1
            )T2 GROUP by  T2.product_id, T2.warehouse_id
        )T3 
            INNER JOIN product on product.id =T3.product_id 
            INNER JOIN warehouse on warehouse.id= T3.warehouse_id
        where T3.qty > 0;
    """ % filter
    rows = []
    try:
        result = db.engine.execute(query)
        for row in result:
            rows.append({
                'qty': int(row[0]),
                'product_id': row[1],
                'product_name': row[2],
                'warehouse_id': row[3],
                'warehouse_name': row[4],
            })
        if len(rows) == 0:
            raise Exception("Stock not found")
    except Exception as e:        
        return e
    return rows