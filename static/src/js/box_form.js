odoo.define("boxwise_wms.box_form", function(require) {
    "use strict";

    var core = require("web.core");
    var Widget = require("web.Widget");
    var User = require("box.classes").User;

    var qweb = core.qweb;
    require("web.dom_ready");

    // The controller
    var box_form = Widget.extend({
        template: "box_form",
        xmlDependencies: ["/boxwise_wms/static/src/xml/box_form.xml"],
        events: {
            "change #ProductCategory": "_onChangeCategory",
            "change #ProductSubcategory": "_onChangeSubcategory",
            "change #ProductTemplate": "_onChangeProduct"
        },
        init: function(parent, options) {
            this._super.apply(this, arguments);
            this.user = new User({ id: odoo.session_info.user_id });
        },
        willStart: function() {
            return $.when(
                this._super.apply(this, arguments),
                this.user.fetchUserInfo(),
                this.user.fetchAllCategories(),
                this.user.fetchAllProducts(),
                this.user.fetchAllAttributeLines(),
                this.user.fetchAllAttributes(),
                this.user.fetchAllAttributeValues()
            );
        },
        start: function() {
            var self = this;
            return this._super.apply(this, arguments).then(function() {
                console.log(self.user);
                self.SelectCategory = new BoxSelectField(self, {
                    id: "ProductCategory",
                    name: "Category",
                    placeholder: "Select a Category",
                    iterator: [],
                    selected: 0,
                    visible: true
                });
                for (var cat_id in self.user.categories) {
                    self.SelectCategory.iterator.push(
                        self.user.categories[cat_id]
                    );
                }
                self.SelectCategory.appendTo($(".o_select_category"));
                self.SelectCategory._select2();
                self.SelectSubcategory = new BoxSelectField(self, {
                    id: "ProductSubcategory",
                    name: "Subcategory",
                    placeholder: "Filter further ..",
                    iterator: [],
                    selected: 0,
                    visible: false
                });
                self.SelectSubcategory.appendTo($(".o_select_subcategory"));
                self.SelectProduct = new BoxSelectField(self, {
                    id: "ProductTemplate",
                    name: "Product",
                    placeholder: "Select a Product",
                    iterator: [],
                    selected: 0,
                    visible: false
                });
                self.SelectProduct.appendTo($(".o_select_product"));
                self.AttributeGroup = new BoxAttributeGroup(self, {
                    iterator: [],
                    visible: false
                });
                self.AttributeGroup.appendTo($(".o_select_attributes"));
                self.BoxFormEnd = new BoxFormEnd(self);
                self.BoxFormEnd.appendTo($(".o_end_of_form"));
            });
        },
        _rerender: function() {
            this.replaceElement(qweb.render("box_form", { widget: this }));
        },

        // At the moment we are saving data in the component.
        // ----------------ToDo seperate data from component
        _calcProducts: function() {
            this.SelectProduct.iterator = [];
            var cats = [];
            if (this.SelectSubcategory.selected) {
                cats.push(this.SelectSubcategory.selected);
            } else {
                cats.push(this.SelectCategory.selected);
                for (var cat_id in this.user.subcategories) {
                    if (
                        this.user.subcategories[cat_id].parent_id ==
                        this.SelectCategory.selected
                    ) {
                        cats.push(parseInt(cat_id));
                    }
                }
            }
            for (var prod_id in this.user.products) {
                if (
                    jQuery.inArray(
                        this.user.products[prod_id].categ_id,
                        cats
                    ) >= 0
                ) {
                    this.SelectProduct.iterator.push(
                        this.user.products[prod_id]
                    );
                }
            }
        },

        // ------------TODO Refactor Change events
        _onChangeCategory: function() {
            this.SelectCategory.selected = parseInt(
                $("#" + this.SelectCategory.id)[0].value
            );
            this.SelectSubcategory.selected = 0;
            this.SelectSubcategory.visible = false;
            this.SelectSubcategory.iterator = [];
            this.SelectProduct.selected = 0;
            this.SelectProduct.visible = false;
            if (this.SelectCategory.selected) {
                for (var subcat_id in this.user.subcategories) {
                    if (
                        this.user.subcategories[subcat_id].parent_id ==
                        this.SelectCategory.selected
                    ) {
                        this.SelectSubcategory.iterator.push(
                            this.user.subcategories[subcat_id]
                        );
                    }
                }
                if (this.SelectSubcategory.iterator.length) {
                    this.SelectSubcategory.visible = true;
                }
                this._calcProducts();
                this.SelectProduct.visible = true;
            }
            this.SelectCategory._rerender();
            this.SelectSubcategory._rerender();
            this.SelectProduct._rerender();
            this.AttributeGroup._destroySelectFields();
            this.BoxFormEnd.visible = false;
            this.BoxFormEnd._rerender();
        },
        _onChangeSubcategory: function() {
            this.SelectSubcategory.selected = parseInt(
                $("#" + this.SelectSubcategory.id)[0].value
            );
            this.SelectProduct.selected = 0;
            this._calcProducts();
            this.SelectSubcategory._rerender();
            this.SelectProduct._rerender();
            this.AttributeGroup._destroySelectFields();
            this.BoxFormEnd.visible = false;
            this.BoxFormEnd._rerender();
        },
        _onChangeProduct: function() {
            this.SelectProduct.selected = parseInt(
                $("#" + this.SelectProduct.id)[0].value
            );
            if (this.SelectProduct.selected) {
                this.AttributeGroup.visible = true;
                this.AttributeGroup.iterator = this.user.linkAttributes(
                    this.SelectProduct.selected
                );
                this.AttributeGroup._createSelectFields();
                this.BoxFormEnd.visible = true;
            } else {
                this.AttributeGroup._destroySelectFields();
                this.BoxFormEnd.visible = false;
            }
            console.log(this.BoxFormEnd);
            this.SelectProduct._rerender();
            this.AttributeGroup._rerender();
            this.BoxFormEnd._rerender();
        }
    });

    // Widget / Component for Select Fields
    var BoxSelectField = Widget.extend({
        template: "box_select_field",
        xmlDependencies: ["/boxwise_wms/static/src/xml/box_form.xml"],
        init: function(parent, values) {
            this._super.apply(this, arguments);
            for (let key in values) {
                this[key] = values[key];
            }
        },
        _select2() {
            $("#"+this.id).select2({
                theme: "bootstrap",
                placeholder: this.placeholder,
                allowClear: true,
            });
        },
        _rerender: function() {
            this.replaceElement(
                qweb.render("box_select_field", { widget: this })
            );
            this._select2();
        }
    });

    // Widget / Component for dynamic Attribute generation
    var BoxAttributeGroup = Widget.extend({
        template: "box_attribute_group",
        xmlDependencies: ["/boxwise_wms/static/src/xml/box_form.xml"],
        init: function(parent, values) {
            this._super.apply(this, arguments);
            for (let key in values) {
                this[key] = values[key];
            }
            this.selectFields = [];
            console.log(this);
        },
        _rerender: function() {
            this.replaceElement(
                qweb.render("box_attribute_group", { widget: this })
            );
        },
        _createSelectFields: function() {
            this.selectFields = [];
            for (var att of this.iterator) {
                this.selectFields.push(
                    new BoxSelectField(self, {
                        id: "Attribute" + att.id,
                        name: att.name,
                        placeholder: "Select a " + att.name,
                        iterator: att.attribute_values,
                        selected: 0,
                        visible: true
                    })
                );
            }
        },
        _destroySelectFields: function() {
            this.visible = false;
            this.iterator = [];
            for (var selfield of this.selectFields) {
                selfield.destroy(); //not sure if working
            }
            this.selectFields = [];
            this._rerender();
        }
    });

    // Widget / Component of last input fields and the submit button
    var BoxFormEnd = Widget.extend({
        template: "box_form_end",
        xmlDependencies: ["/boxwise_wms/static/src/xml/box_form.xml"],
        init: function(parent) {
            this._super.apply(this, arguments);
            this.visible = false;
        },
        _rerender: function() {
            this.replaceElement(qweb.render("box_form_end", { widget: this }));
        }
    });

    var $elem = $(".o_box_form");
    var box_form_instance = new box_form(null);
    box_form_instance.appendTo($elem);
});
