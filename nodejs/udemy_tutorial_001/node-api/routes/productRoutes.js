const express = require('express');
const router = express.Router();
const productController = require('../controller/productController');
const joiSchemaValidation = require('../middleware/joiSchemaValidation');
const productSchema = require('../apiSchema/productSchema');
const tokenValidation = require('../middleware/tokenValidation');

router.post('/',
  tokenValidation.validateToken,
  joiSchemaValidation.validateBody(productSchema.createProductSchema),
  productController.createProduct
);

router.get('/:id',
  tokenValidation.validateToken,
  productController.getProductById
);

router.put('/:id',
  tokenValidation.validateToken,
  joiSchemaValidation.validateBody(productSchema.updateProductSchema),
  productController.updateProduct
);

router.get('/',
  tokenValidation.validateToken,
  joiSchemaValidation.validateQueryParams(productSchema.getAllProductSchema),
  productController.getAllProducts
);

router.delete('/:id',
  tokenValidation.validateToken,
  productController.deleteProduct
)

module.exports = router;