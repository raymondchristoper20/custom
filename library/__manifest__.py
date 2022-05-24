{
'name': 'Idea', #nama modul yg dibaca user di UI
'version': '1.0',
'author': 'Raymond',
'summary': 'Modul Idea SIB UK Petra', #deskripsi singkat dari modul
'description': 'Library management module', #bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
#di idea/static/description, bisa kasi icon modul juga.
'category': 'Latihan',
'website': 'http://sib.petra.ac.id',
'depends': ['base', 'sales_team'], # list of dependencies, conditioning startup order
'data': [ 'views/book_views.xml', 'views/sale_order_views2.xml', 'views/transaction_views.xml', 'security/ir.model.access.csv'],
'qweb':[], #untuk memberi tahu tempat static file, misal CSS, javascript – html yang lgs dijalnkan (jk ada)
'demo': ['demo/demo.xml'], # demo data (for unit tests)
'installable': True,
'auto_install': False, # indikasi install, saat buat database baru
}