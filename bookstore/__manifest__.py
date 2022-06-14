{
'name': 'Book Store', #nama modul yg dibaca user di UI
'version': '1.0',
'author': 'Raymond',
'summary': 'Modul Toko Buku', #deskripsi singkat dari modul
'description': 'Book Store management module', #bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
#di idea/static/description, bisa kasi icon modul juga.
'category': 'Latihan',
'website': 'http://sib.petra.ac.id',
'depends': ['base', 'sales_team'], # list of dependencies, conditioning startup order
'data': [ 'views/book_views.xml',
          'views/author_views.xml',
          'views/publisher_views.xml',
        'views/transaction_views.xml',
        'views/customer_views.xml',
          'data/ir_sequence_data.xml',
          'wizard/wiz_discount_views.xml',
          'security/ir.model.access.csv'],
'qweb':[], #untuk memberi tahu tempat static file, misal CSS, javascript – html yang lgs dijalnkan (jk ada)
'demo': ['demo/demo.xml'], # demo data (for unit tests)
'installable': True,
'auto_install': False, # indikasi install, saat buat database baru
}