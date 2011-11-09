(function($) {
	
	window.Address = Backbone.Model.extend({});
	
	window.Addresses = Backbone.Collection.extend({
		model: Address,
		url: '/addresses'
	});
	
	window.addressBook = new Addresses();
	
	window.AddressView = Backbone.View.extend({
		tagName: 'li',
		
		events: {
			'click a.delete': 'delete'
		},
		
		initialize: function() {
			_.bindAll(this, 'render');
			this.model.bind('change', this.render);
			this.model.bind('destroy', this.remove, this);
			this.template = _.template($('#address-template').html());
		},
		
		render: function() {
			var renderedContent = this.template(this.model.toJSON());
			$(this.el).html(renderedContent);
			return this;
		},
		
		delete: function() {
			this.model.destroy();
		},
		
		remove: function() {
      $(this.el).remove();
    }
	});
	
	window.AddressBookItemView = AddressView.extend({
	});
	
	window.AddressBookView = Backbone.View.extend({
		events: {
			'click #create': 'create'
		},
		
		initialize: function() {
			_.bindAll(this, 'render');
			this.template = _.template($('#address-book-template').html());
			this.collection.bind('reset', this.render);
			this.collection.bind('add', function(addr) {
			  addr.save();
				this.render();
			}, this);
		},

		render: function() {
			var $addresses, 
					collection = this.collection;

			$(this.el).html(this.template({}));
			$addresses = this.$('.addresses');
			collection.each(function(address) {
				var view = new AddressBookItemView({
					model: address,
					collection: collection
				});
				$addresses.append(view.render().el);
			});

			return this;
		},
		
		create: function() {
			new_address = this.collection.add({nickname: $('input#nickname').val(), location: $('input#location').val()});
		}
	});
	
	window.BackboneUber = Backbone.Router.extend({
		routes: {
			'': 'home'
		},
		
		initialize: function () {
			this.addressBookView = new AddressBookView({
				collection: window.addressBook
			});
		},
		
		home: function() {
			$('#container').empty();
			$('#container').append(this.addressBookView.render().el);
		}
	});
	
	$(function() {
		window.App = new BackboneUber();
		Backbone.history.start();
		
	});
	
})(jQuery);