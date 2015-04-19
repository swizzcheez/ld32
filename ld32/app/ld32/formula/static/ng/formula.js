
angular.module('FormulaView', ['ngResource'])

//////////////////////////////////////////////////////////////////////////////

.controller('FormulaSelectionCtrl',
function($scope)
{
    this.selectable = { }

    this.start = function(opname, op)
    {
        this.op = op
        this.step = 0
        this.nextArg()
        this.args = [opname]
    }

    this.nextArg = function()
    {
        if (this.step < this.op.arguments.length)
        {
            this.workarg = this.op.arguments[0]
            this.argument = ''
            this.step++
            var selectable = this.selectable = {}
            angular.forEach(this.workarg.selects,
            function(code)
            {
                selectable[code] = true
            })
        }
        else
        {
            $scope.view_url += this.args.join(';') + '/'
            this.cancel()
        }
    }

    this.selectNode = function(node)
    {
        // WSGI (and others) will convert %2F into path separator
        // sometimes. 
        this.args.push(encodeURIComponent(node.repr.replace('/', '$2F')))
        this.nextArg()
    }

    this.nodeIsSelectable = function(node)
    {
        var check = this.selectable
        return check 
               && node.extra.length 
               && !node.extra.every(function(key) { return !check[key] })
    }

    this.cancel = function()
    {
        this.op = null
        this.selectable = []
    }
})

//////////////////////////////////////////////////////////////////////////////

.directive('formulaLoader',
function($resource)
{
    return {
        restrict: 'AE',
        scope:
        {
            into: '=',
            formula_url: '=url',
        },
        link: function($scope, $element, $attrs)
        {
            $scope.$watch('formula_url',
            function(url)
            {
                $scope.into = $resource(url).get()
            })
        }
    }
})

//////////////////////////////////////////////////////////////////////////////

.directive('formulaView',
function()
{
    return {
        restrict: 'AE',
        require: [ 'formulaView', '?^^formulaView' ],
        templateUrl: '/static/formula/ng/tpl/node.html',
        scope:
        {
            node: '=',
            child_css: '@innerClass',
            isSelectable: '&',
            onSelect: '&'
        },
        controller: function($scope, $element)
        {
        },
        link: function($scope, $element, $attrs, requires)
        {
            var ctrl = requires[0]
            var node = ctrl.node = $scope.node
            ctrl.onSelect = $scope.onSelect
            ctrl.isSelectable = $scope.isSelectable
            var parent = requires[1]
            if (parent != null)
            {
                angular.extend(ctrl, parent)
            }
            $scope.onSelect = ctrl.onSelect
            $scope.isSelectable = ctrl.isSelectable
            var css_classes = $scope.css_classes = [ 'node-' + node.type ]
            angular.forEach(node.extra,
            function(code)
            {
                css_classes.push("node-" + code)
            })
        }
    }
})

; // End of module



