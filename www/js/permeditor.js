/* Constructor. Options is a dictionary.
 * Expected options:
 * - selectorId: The id of the ul to add f.i. every group and the
 *   	dropdown with all the remaining groups to.
 * - urlPrefix: The name of the current item is added to this prefix to link
 *   	to f.i. a group
 * - init: callback-function which returns two lists in a dictionary:
 *   	added and addable. The first being the list with the items which are
 *   	already part of the PermissionsEditor, and addable items which can be added.
 *   	This method is also called when re-initializing after a change.
 * - addCallback: callback-function, expecting the name of the item to be
 *   	added. This usually does an Ajax-request to add f.i. a user to a group.
 * - removeCallback: Analogous to addCallback, only for removing. Also expects
 *   	the name of the item to be removed.
 * - canLink: is a user allowed to see a link to the other object? This is a
 *   	function, expecting the name of the current object.
 */
function PermissionsEditor(options) {
	this.options = options;
	this.list = document.getElementById(this.options.editorId);
	this.init();
}

/* Creates the add/remove button for each item */
PermissionsEditor.prototype.makeButton = function(className) {
	var link = $c("a", {"href": "#", "className": className});
	var imgSrc = media_url + "/img/" +
		(className == "remover" ? "min.gif" : "plus.gif");
	var img = $c("img", {"src": imgSrc, "className": className});
	link.appendChild(img);
	return link;
}

/* Reinitializes the list after a change. */
PermissionsEditor.prototype.reInit = function() {
	// Make the list empty before calling init().
	for (var item_idx=this.list.childNodes.length; item_idx--;)
		this.list.removeChild(this.list.childNodes[item_idx]);
	this.init();
}

function permissionSort(a, b)
{
	if (a.type == b.type) {
		if (a.name < b.name)
			return -1;
		return 1;
	}

	if (a.type > b.type)
		return 1;
	return -1;
}

PermissionsEditor.prototype.init = function() {
	var callbackValue = this.options.initCallback(this.options.path);

	for (var item_idx=this.list.childNodes.length; item_idx--;)
		this.list.removeChild(this.list.childNodes[item_idx]);

	// The li-items
	var added = callbackValue["added"];
	added.sort(permissionSort);
	for (var added_idx=0; added_idx < added.length; ++added_idx)
		this.setupAddedItem(added[added_idx]);

	// The dropdown
	var addable = callbackValue["addable"];
	addable.sort(permissionSort);
	this.setupSelect();
	for (var addable_idx=0; addable_idx < addable.length; ++addable_idx)
		this.addOption(addable[addable_idx]);
	if (!addable.length)
		this.disableSelect();
}

PermissionsEditor.prototype.permissionsSelect = function(name, type, permissions) {
	var select = $c("select");
	var values = ['', 'r', 'rw'];
	for (var idx = 0; idx < values.length; ++idx) {
		select.appendChild($c("option", {'value': values[idx], 'innerHTML': values[idx]}));
		if (values[idx] == permissions)
			select.selectedIndex = idx;
	}
	var _this = this;
	select.onchange = function() {
		var permissions = values[parseInt(select.selectedIndex)];
		_this.options.changeCallback(name, type, permissions, _this.options.path);
		_this.reInit();
		return false;
	};
	return select;
}

PermissionsEditor.prototype.setupAddedItem = function(added) {
		var item = $c("li", {'name': added['name']});
		var permissions = added['permissions'];
		if (permissions == '')
			permissions = 'none';
		var type = added['type'];
		var name = added['name'];

		var displayname = '[' + type + '] ' + name;
		item.appendChild($c("label", {"innerHTML": displayname}));
		item.appendChild(this.permissionsSelect(name, type, permissions));

		var remover = this.makeButton("remover");
		item.appendChild(remover);

		var _this = this; // this is out of scope in onclick below!
		remover.onclick = function() {
			var name = this.parentNode.name;
			_this.options.removeCallback(name, type, _this.options.path);
			_this.reInit();
			return false;
		};

		this.list.appendChild(item);
}

PermissionsEditor.prototype.disableSelect = function() {
	this.select.disabled = true;

	// Disable the add-button and change the cursor-style. Maybe hide?
	this.select.adder.disabled_onclick = this.select.adder.onclick;
	this.select.adder.onclick = function() { return false; }
	this.select.adder.style.cursor = 'default';
}

PermissionsEditor.prototype.setupSelect = function() {
	this.select = $c("select");
	var item = $c("li");
	item.appendChild(this.select);
	var adder = this.makeButton("adder");
	this.select.adder = adder;
	var _this = this; // this is out of scope in onclick below!

	adder.onclick = function() {
		var select = _this.select
		var groupname = select.options[select.selectedIndex].getAttribute('value');
		var displayname = select.options[select.selectedIndex].innerHTML;

		if (groupname == "---") {
			Log('Please select an item first', false)
			return false;
		}

		var type = 'user';
		if (displayname.indexOf('[Group] ') != -1)
			type = 'group';

		_this.options.addCallback(groupname, type, _this.options.path);
		_this.reInit();
		return false;
	}
	item.appendChild(adder);
	this.list.appendChild(item);
	this.addOption({'type': '', 'name': "---"});
}

PermissionsEditor.prototype.addOption = function(dict) {
	var option = $c("option", {'value': dict.name});
	var displayname;
	if (dict.type == 'group') {
		displayname = '[Group] ' + dict.name.substring(0, dict.name.length);
	} else if (dict.type == "user") {
			displayname = '[User] ' + dict.name;
	} else {
		displayname = dict.name;
	}

	option.appendChild(document.createTextNode(displayname));
	this.select.appendChild(option);
}