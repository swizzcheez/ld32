
angular.module('Warmup', ['ngRoute', 'ngResource', 'Stage'])

//////////////////////////////////////////////////////////////////////////////

.config([ '$routeProvider',
function($routeProvider)
{
    $routeProvider
        .when('/setup',
        {
            templateUrl: '/static/warmup/ng/tpl/setup.html',
        })
        .when('/playing',
        {
            templateUrl: '/static/warmup/ng/tpl/playing.html',
        })
        .otherwise({
            redirectTo: '/setup'
        })
} ])

//////////////////////////////////////////////////////////////////////////////

.directive('warmupGame', 
function(Set, Actor)
{
    return {
        restrict: 'AE',
        scope:
        {
            into: '=warmupGame',
        },
        controller: function($scope)
        {
            this.set = new Set()
            this.player = new Actor()
            this.monster = new Actor()
        },
        link: function($scope, $element, $attr, ctrl)
        {
            $scope.into = ctrl
        }
    }
})

//////////////////////////////////////////////////////////////////////////////

.directive('warmupLoader',
function()
{
    return {
        restrict: 'AE',
        require: [ '^warmupGame'],
        scope:
        {
            url: '@',
        },
        link: function($scope, $element, $attr, requires)
        {
            console.log(requires)
        }
    }
})

//////////////////////////////////////////////////////////////////////////////

.service('WarmupSet',
function(Set)
{
    function WarmupSet()
    {
    }

    WarmupSet.prototype = angular.extend(
        Set.prototype,
        {
        })

    return WarmupSet
})

//////////////////////////////////////////////////////////////////////////////

.service('Player',
function(Actor)
{
    function Player()
    {
    }

    Player.prototype = angular.extend(
        Actor.prototype,
        {
        })

    return Player
})

//////////////////////////////////////////////////////////////////////////////

.service('Monster',
function(Actor)
{
    function Monster()
    {
    }

    Monster.prototype = angular.extend(
        Actor.prototype,
        {
        })

    return Monster
})

//////////////////////////////////////////////////////////////////////////////

; // End of module

