
angular.module('Stage', [])

//////////////////////////////////////////////////////////////////////////////

.directive('stage',
function()
{
    return {
        restrict: 'AE',
        scope:
        {
            set: '=',
        },
        controllerAs: 'stage',
        controller: function()
        {
        },
        link: function($scope, $element, $attr, ctrl)
        {
            ctrl.set = $scope.set
            $element.css({
                position: 'relative'
            })
        }
    }
})

//////////////////////////////////////////////////////////////////////////////

.directive('puppet',
function()
{
    return {
        restrict: 'AE',
        transclude: true,
        template: '<ng-transclude></ng-transclude>',
        require: [ 'puppet', '^^stage' ],
        scope:
        {
            actor: '=',
        },
        conrollerAs: 'puppet',
        controller: function($scope, $element)
        {
            this.bind_css = function(field, style)
            {
                $scope.$watch('actor.' + field,
                    function(value) { $element.css( style, value) })
            }
        },
        link: function($scope, $element, $attr, requires)
        {
            var ctrl = requires[0]
            ctrl.actor = $scope.actor
            ctrl.stage = requires[1]
            ctrl.set = ctrl.stage.set
            $element.css({
                position: 'absolute'
            })

            ctrl.bind_css('x', 'left')
            ctrl.bind_css('y', 'top')
            ctrl.bind_css('width', 'width')
            ctrl.bind_css('height', 'height')
        }
    }
})

//////////////////////////////////////////////////////////////////////////////

.service('Actor',
function()
{
    function Actor(options)
    {
        options = options || {}
        this.x = options.left || 0
        this.y = options.top ||  0
        this.width = options.width || 0
        this.height = options.height || 0
    }

    Actor.prototype =
    {
        move: function(dx, dy, dt)
        {
            this.x += dx
            this.y += dy
        }
    }

    return Actor
})

//////////////////////////////////////////////////////////////////////////////

.service('Set',
function()
{
    return function Set(options)
    {
        options = options || {}
        this.width = 0
        this.height = 0
    }
})

//////////////////////////////////////////////////////////////////////////////

; // End of module
