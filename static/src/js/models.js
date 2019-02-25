odoo.define("box.classes", function(require) {
    "use strict";

    var Class = require("web.Class");
    var rpc = require("web.rpc");

    var Category = Class.extend({
        init: function(values) {
            Object.assign(this, values);
            this.selected = false;
        }
    });
    var Product = Class.extend({
        init: function(values) {
            Object.assign(this, values);
        }
    });
    var AttributeLine = Class.extend({
        init: function(values) {
            Object.assign(this, values);
        }
    });
    var Attribute = Class.extend({
        init: function(values) {
            Object.assign(this, values);
        }
    });
    var AttributeValue = Class.extend({
        init: function(values) {
            Object.assign(this, values);
        }
    });
    var SelectField = Class.extend({
        init: function(values) {
            Object.assign(this, values);
        }
    });

    var User = Class.extend({
        init: function(values) {
            Object.assign(this, values);
            this.categories = {};
            this.subcategories = {};
            this.products = {};
            this.attribute_lines = {};
            this.attributes = {};
            this.attribute_values = {};
            this.req_attributes = {};
        },
        fetchUserInfo: function() {
            var self = this;
            return rpc
                .query({
                    model: "res.users",
                    method: "read",
                    args: [[this.id]],
                    kwargs: { fields: ["id", "login", "name"] }
                })
                .then(function(user_values) {
                    var values = user_values[0];
                    Object.assign(self, values);
                    return self;
                });
        },
        fetchAllCategories: function() {
            var self = this;
            return rpc
                .query({
                    model: "product.category",
                    method: "search_read",
                    args: [[]],
                    kwargs: { fields: ["id", "name", "child_id", "display_name"] }
                })
                .then(function(cats) {
                    for (var cat of cats) {
                        if (cat.child_id.length<1) {
                            cat.name = cat.display_name.substring(6)
                            self.categories[cat.id] = new Category(cat);
                        }
                    }
                    return self;
                });
        },
        fetchAllProducts: function() {
            var self = this;
            return rpc
                .query({
                    model: "product.template",
                    method: "search_read",
                    args: [[]],
                    kwargs: {
                        fields: ["id", "name", "categ_id", "attribute_line_ids"]
                    }
                })
                .then(function(prods) {
                    for (var prod of prods) {
                        prod.categ_id = prod.categ_id[0];
                        self.products[prod.id] = new Product(prod);
                    }
                    return self;
                });
        },
        fetchAllAttributeLines: function() {
            var self = this;
            return rpc
                .query({
                    model: "product.attribute.line",
                    method: "search_read",
                    args: [[]],
                    kwargs: {
                        fields: [
                            "id",
                            "product_tmpl_id",
                            "attribute_id",
                            "value_ids"
                        ]
                    }
                })
                .then(function(attlins) {
                    for (var attlin of attlins) {
                        self.attribute_lines[attlin.id] = new AttributeLine(
                            attlin
                        );
                    }
                    return self;
                });
        },
        fetchAllAttributes: function() {
            var self = this;
            return rpc
                .query({
                    model: "product.attribute",
                    method: "search_read",
                    args: [[]],
                    kwargs: {
                        fields: [
                            "id",
                            "name",
                            "attribute_line_ids",
                            "value_ids"
                        ]
                    }
                })
                .then(function(atts) {
                    for (var att of atts) {
                        self.attributes[att.id] = new Attribute(att);
                    }
                    return self;
                });
        },
        fetchAllAttributeValues: function() {
            var self = this;
            return rpc
                .query({
                    model: "product.attribute.value",
                    method: "search_read",
                    args: [[]],
                    kwargs: {
                        fields: ["id", "name", "attribute_id", "product_ids"]
                    }
                })
                .then(function(attvals) {
                    for (var attval of attvals) {
                        self.attribute_values[attval.id] = new AttributeValue(
                            attval
                        );
                    }
                    return self;
                });
        },
        // This is actually just a join Query.
        linkAttributes: function(prod_id) {
            var req_attributes = [];
            for (var attlin_id of this.products[prod_id].attribute_line_ids) {
                var tmp = this.attributes[this.attribute_lines[attlin_id].attribute_id[0].toString()];
                tmp.attribute_values = [];
                for (var att_val_id of this.attribute_lines[attlin_id].value_ids){
                    tmp.attribute_values.push(this.attribute_values[att_val_id]);
                }
                req_attributes.push(tmp);
            }
            return req_attributes;
        }
    });

    return {
        Category: Category,
        Product: Product,
        Attribute: Attribute,
        AttributeValue: AttributeValue,
        User: User
    };
});
