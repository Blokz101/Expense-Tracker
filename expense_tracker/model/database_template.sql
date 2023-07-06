CREATE TABLE "transactions"(
    "id" INTEGER NOT NULL PRIMARY KEY,
    "description" TEXT NOT NULL,
    "merchant_id" BIGINT NOT NULL,
    "date" DATE NOT NULL,
    "amount" DOUBLE(8, 2) NOT NULL,
    "reconciled_status" TINYBIGINT(1) NOT NULL DEFAULT '0',
    "statement_name" TEXT NULL,
    "receipt_photo_path" TEXT NULL,
    "x_coord" DOUBLE(8, 8) NULL,
    "y_coord" DOUBLE(8, 8) NULL,
    FOREIGN KEY ("merchant_id") REFERENCES "merchants"("id")
);

CREATE TABLE "transaction_tag_branch"(
    "id" INTEGER NOT NULL PRIMARY KEY,
    "transaction_id" BIGINT NOT NULL,
    "tag_id" BIGINT NOT NULL,
    FOREIGN KEY ("tag_id") REFERENCES "tags"("id"),
    FOREIGN KEY ("transaction_id") REFERENCES "transactions"("id")
);

CREATE TABLE "tags"(
    "id" INTEGER NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL
);

CREATE TABLE "merchant_tag_branch"(
    "id" INTEGER NOT NULL PRIMARY KEY,
    "merchant_id" BIGINT NOT NULL,
    "tag_id" BIGINT NOT NULL,
    FOREIGN KEY ("merchant_id") REFERENCES "merchants"("id"),
    FOREIGN KEY ("tag_id") REFERENCES "tags"("id")
);

CREATE TABLE "merchants"(
    "id" INTEGER NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL
);

CREATE TABLE "merchant_locations"(
    "id" INTEGER NOT NULL PRIMARY KEY,
    "merchant_id" BIGINT NOT NULL,
    "x_coord" DOUBLE(8, 8) NOT NULL,
    "y_coord" DOUBLE(8, 8) NOT NULL,
    FOREIGN KEY ("merchant_id") REFERENCES "merchants"("id")
);
