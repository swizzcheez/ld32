
angular.module('FormulaView', ['ngResource'])

//////////////////////////////////////////////////////////////////////////////

.directive('formulaLoader',
function($resource)
{
    return {
        restrict: 'AE',
        scope:
        {
            into: '='
        },
        link: function($scope, $element, $attrs)
        {
            $scope.into = $resource($attrs.url).get()
        }
    }
})

//////////////////////////////////////////////////////////////////////////////

.directive('formulaView',
function()
{
    return {
        restrict: 'AE',
        template: '<span ng-include=\'"/static/formula/ng/tpl/" '
                  + '+ node.type_code + ".html"\' ng-if="node"></span>',
        scope:
        {
            node: '='
        },
    }
})

; // End of module



