
angular.module('Game', [])

//////////////////////////////////////////////////////////////////////////////

.directive('playfield',
function(Playfield, $timeout)
{
    return {
        restrict: 'AE',
        scope: 
        {
            playfield: '=',
        },
        controllerAs: 'playfield',
        controller: function()
        {
        },
        link: function($scope, $element, $attr, ctrl)
        {
            ctrl.model = $scope.playfield || new Playfield()
            ctrl.model.update()
            
            function tick()
            {
                // TODO: Better time management
                var dt = ctrl.model.update(Date.now())
                $timeout(tick, Math.max(0, 30 - dt))
            }
            $timeout(tick, 30)
        }
    }
})

//////////////////////////////////////////////////////////////////////////////

.factory('Playfield',
function()
{
    function Playfield()
    {
        this.sprites = {}
    }

    Playfield.prototype =
    {
        addSprite: function(sprite)
        {
            this.sprites.push(sprite)
            sprite.update(this, null)
        },

        update: function(t)
        {
            var dt = t - this.now
            this.now = t
            angular.forEach(this.sprites,
            function(sprite)
            {
                sprite.update(this, dt)
            })
            return dt
        }
    }

    return Playfield
})

//////////////////////////////////////////////////////////////////////////////

.directive('sprite',
function(Sprite)
{
    return {
        restrict: 'AE',
        transclude: true,
        require: [ 'sprite', '^^playfield' ],
        template: function(element, attrs)
        {
            if (attrs.url)
            {
                return '<ng-include src=\'"' + attrs.url + '"\'></ng-include>'
            }
            else
            {
                return '<ng-transclude></ng-transclude>'
            }
        },
        scope: {
            onCreate: '&',
            sprite:  '=',
            url: '@',
            handle: '@',
            handleX: '@',
            handleY: '@',
        },
        controllerAs: 'sprite',
        controller: function($scope)
        {
            this.setSprite = function(sprite, playfield)
            {
                this.model = sprite
                this.playfield = playfield
            }

            this.setElement = function(element)
            {
                this.element = element
            }

            this.setHandle = function()
            {
                var handle = Sprite.pos2pct.apply(this, arguments)
                this.element.attr('margin-left', '-' + handle.left)
                this.element.attr('margin-top', '-' + handle.top)
            }
        },
        link: function($scope, $element, $attrs, requires)
        {
            var ctrl = requires[0]
            var playfield = requires[1].model
            var sprite = $scope.sprite || new Sprite()

            ctrl.setSprite(sprite, playfield)
            ctrl.setElement($element)
            ctrl.setHandle($scope.handle, $scope.handleX, $scope.handleY)
            $scope.onCreate({ sprite: sprite })
        }
    }
})

//////////////////////////////////////////////////////////////////////////////

.factory('Sprite',
function()
{
    function Sprite()
    {
    }

    Sprite.prototype =
    {
    }

    Sprite.pos2pct = function()
    {
        var pos_top, pos_left;
        if (arguments.length == 1 || arguments.length == 3)
        {
            switch (arguments[0])
            {
                case 'top':
                case 'north':
                    pos_left = '50%'; pos_top = '0%'; break;
                case 'right':
                case 'east':
                    pos_left = '100%'; pos_top = '50%'; break;
                case 'bottom':
                case 'south':
                    pos_left = '0%'; pos_top = '100%'; break;
                case 'left':
                case 'best':
                    pos_left = '0%'; pos_top = '50%'; break;
                case 'nw':
                    pos_left = '0%'; pos_top = '0%'; break;
                case 'ne':
                    pos_left = '0%'; pos_top = '100%'; break;
                case 'se':
                    pos_left = '100%'; pos_top = '100%'; break;
                case 'sw':
                    pos_left = '0%'; pos_top = '100%'; break;
                default:
                case 'center':
                    pos_left = '50%'; pos_top = '50%'; break;
            };
            if (arguments[1] != null)
            {
                pos_left = arguments[1]
            }
            if (arguments[2] != null)
            {
                pos_top = arguments[2]
            }
            return { top: pos_top, left: pos_left };
        }
        else
        {
            return { top: arguments[1], left: arguments[0] };
        }
    }

    return Sprite
})

; // End of module
