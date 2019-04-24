document.addEventListener("DOMContentLoaded", function(event) { 
    const MOD_CONTAINER = "mod-container";
    const MOD = "griditem-mod";

    function findImage(imgs, style) {
        var target_height = parseInt(style.height);
        var target_width = parseInt(style.width);

        for(var i = 0; i < imgs.length; i++) {
            var img = imgs[i];
            if ((img.height == target_height) && (img.width == target_width)) {
                return img;
            }
        }

        return imgs[0];
    }

    var containers = document.getElementsByClassName(MOD_CONTAINER);
    for(var c = 0; c < containers.length; c++) {
        var container = containers[c];
        var mods = container.getElementsByClassName(MOD);
        for(var m = 0; m < mods.length; m++) {
            var mod = mods[m];
            var imgs = mod.getElementsByTagName("img");
            var img = imgs[0];
            if (imgs.length > 0) {
                img = findImage(imgs, window.getComputedStyle(mod));
            }
            mod.style.backgroundImage = "url(\"" + img.src + "\")";
        }
    }
});
