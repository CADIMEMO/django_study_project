SELECT "shopapp_product"."id", "shopapp_product"."name", "shopapp_product"."description", "shop
app_product"."price", "shopapp_product"."discount", "shopapp_product"."created_by_id", "shopapp_product
"."create_at", "shopapp_product"."archieved", "shopapp_product"."preview" FROM "shopapp_product" ORDER
BY "shopapp_product"."name" ASC, "shopapp_product"."price" ASC; args=(); alias=default



SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_supe
ruser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email",
 "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user" WHERE "aut
h_user"."id" = 1 LIMIT 21; args=(1,); alias=default


SELECT ("shopapp_order_products"."order_id") AS "_prefetch_related_val_order_id", "shopapp_prod
uct"."id", "shopapp_product"."name", "shopapp_product"."description", "shopapp_product"."price", "shopa
pp_product"."discount", "shopapp_product"."created_by_id", "shopapp_product"."create_at", "shopapp_prod
uct"."archieved", "shopapp_product"."preview" FROM "shopapp_product" INNER JOIN "shopapp_order_products
" ON ("shopapp_product"."id" = "shopapp_order_products"."product_id") WHERE "shopapp_order_products"."o
rder_id" IN (1, 2) ORDER BY "shopapp_product"."name" ASC, "shopapp_product"."price" ASC; args=(1, 2); a
lias=default
