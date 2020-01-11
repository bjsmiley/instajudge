$(document).ready(function(){

// ----------------------- [START] Ajax Functions -----------------------
    function beginPartOne(username){
        var url = [ "/ajax/search?u=" , username , "&m=instagram-scraper" ].join("")
        $.post(
            url, 
            {},
            function(data, status){
                console.log(status)
                var status_code = data.code
                if( status_code == 201 ){
                    // 201: completed normally, 203: user already has directory of photos
                    console.log( data.message )
                    // if( status_code == 203 ){
                    //     showNextProgress( true )
                    // }
                    //else{
                        showNextProgress( false )
                    //}
                    
                    beginPartTwo( data.url )
                }
                else if( status_code == 404 || status_code == 409 ){
                    // couldnt find the current user or the user is private
                    // stop displaying all progress and show error
                    console.log( data.message )
                    showErrorMessage( status_code )
                }
                // else if( status_code == 202 ){
                //     // 202: the json object already exists
                //     // pause for a second
                //     showNextProgress( false )
                //     // pause for a second
                //     showEndProgress( false )
                //     // update page with tags
                //     console.log( data.message )
                //     displayResults( data.tags )

                // }
                else{
                    // unknown error
                    console.log("Something bad happened")
                    console.log( data )
                    //toggleProgress( 1, "instagram-scraper (Error Ocurred)")
                    errorProgress( 1 , "Something Really Bad Happened (here)")
                }
                

            }
        )
    }

    function beginPartTwo( url ){
        $.post(
            url,
            {},
            function(data, status){
                console.log(status)
                status_code = data.code
                if( status_code == 405 ){
                    // something bad is wrong between the 2 operations, the username 
                    // for this part is not the same as the first part
                    console.log( data.message )
                    showErrorMessage( status_code )
                }
                else if( status_code == 200 || status_code == 202 ){
                    // All Done!
                    console.log( data.message )
                    showEndProgress( false )
                    displayResults( data.tags )


                }
                else{
                    // unknown error
                    console.log("Something bad happened, here")
                    console.log( data )
                    //toggleProgress(2, "clarifai (Error Ocurred)")
                    errorProgress( 2 , "Something Really Bad Happened")
                }
            }
        )
    }

    function displayResults( tags ){
        //console.log( tags )
        html_tags = []
        var len = tags.length
        for( var i = 0 ; i < len ; i++ ){
            var id= "tag-" + i
            badge_string = "<span id='" + id + "' class='badge badge-pill "
            color = "secondary"
            if( tags[i].prob > 0.80 ){
                color = "success"
            }
            else if( tags[i].prob > 0.70 ){
                color = "warning"
            }
            else{
                color = "danger"
            }
            badge_string += "badge-" + color + "' style='cursor:pointer;'>" + tags[i].name + " (" + tags[i].count + ")</span>"
            html_tags.push( badge_string )
            var urls = tags[i].urls
            var tag_name = tags[i].name
            var closureFunction = function(list_of_urls, tag_name){
                $(document).on('click','#'+ id, list_of_urls ,function(){
                    console.log("clicked!", list_of_urls)
                    if( $("#photo-display-section").is(":visible") ){
                        clearPhotoDisplaySection()
                        console.log("herehere")
                    }
                    insertIntoPhotoDisplaySection(tag_name, list_of_urls)
                    if( $("#photo-display-section").is(":hidden") ){
                        showPhotoDisplaySection()
                    }

                    // code to automatically scroll down goes here!
                    //setTimeout(function(){
                    $('html, body').animate({
                        scrollTop: ($('#photo-display-section').offset().top)
                    },200);
                    //}, 1000)
                });
            }

            closureFunction(urls, tag_name)
            
        }

        html_tags_string = html_tags.join(" ")
        showTagSection() // show tag all of the tag section
        clearPhotoDisplaySection() // dont show photo display section
        $("#tag-body").append(html_tags_string)
        $("#profile-section").show() // show profile div

        

        //$(document).scrollTo('#photo-display-section');

        // $('html, body').animate({
        //     scrollTop: ($('#photo-display-section').offset().top)
        // },500);

        // $([document.documentElement, document.body]).animate({
        //     scrollTop: $("#photo-display-section").offset().top
        // }, 2000);

        // $(window).scrollTop( $("#photo-display-section").offset().top )
        
    }
// ----------------------- [ END ] Ajax Functions -----------------------


// ------------------ [START] Manipulate Functions ------------------
function insertIntoPhotoDisplaySection(tag_name, list_of_urls){
    $("#photo-display-title").html(list_of_urls.length + " Photo(s) for <small>" + tag_name + "</small>")
    console.log(list_of_urls)
    $("#photo-display-body").append("<div id='photo-display-preview' class='col-sm-5 text-center' style='max-height:375px; overflow-y:scroll;'></div>")
    $("#photo-display-body").append("<div id='photo-display-selected' class='col-sm text-center'><img id='photo-display-selected-img' class='border border-dark' height='400' width='400'></div>")
    for( var i = 0 ; i < list_of_urls.length ; i++){
        $("#photo-display-preview").append("<img id='photo-preview-"+i+"' class='img-thumbnail preview-images m-2' src='" + list_of_urls[i] + "' height='55' width='55'>")
        console.log("done " + (i+1) + " times" )
    } 
    var closureFunction = function(){
        $(".preview-images").on("mouseover", function(){
            var newSource = $(this).attr('src')
            $("#photo-display-selected-img").attr("src",newSource)
        })
    }
    closureFunction()
    $("#photo-display-selected-img").attr("src",list_of_urls[0])
}
// ------------------ [ END ] Manipulate Functions ------------------





// ------------------ [START] Error Functions ------------------
    function showErrorMessage( code ){
        if( code == 405 ){
            // bad operation
            //toggleProgress( 2 , "clarifai (username between operations dont match)")
            errorProgress( 2 , "Error: username between operations dont match")
            alert("Error: The operation crashed")
            return 
        }
        if( code == 404 ){
            // user not found
            $("#username-error-display").text("Not a valid Instagram username")
            //toggleProgress( 1 , "instagram-scraper (User not found)")
            errorProgress( 1 , "Error: User Not Found")
            return 
        }
        if( code == 409 ){
            $("#username-error-display").text("This user's account is private")
            errorProgress( 1 , "Error: User is private")
        }
    }
// ------------------ [ END ] Error Functions ------------------



// ------------------ [START] Progress Functions ------------------
    function showBeginningProgress(){
        $("#instagram-scraper-loader").text("Collecting Instagram Photos...")
        $("#instagram-scraper-image").attr("src", "/static/progress/Loading.gif")
        $("#instagram-scraper-image").show()
    }

    function showNextProgress( needDelay ){
        if( needDelay ){
            //setTimeout(function(){
            //$("#instagram-scraper-loader").text("Collecting Instagram Photos...")
            $("#instagram-scraper-image").attr("src", "/static/progress/Check-Mark.png")
            //}, 5000)
            $("#clarifai-loader").text("Analyzing Images...")
            $("#clarifai-loader-image").attr("src", "/static/progress/Loading.gif")
        }
        else{
            //$("#instagram-scraper-loader").text("Collecting Instagram Photos...")
            $("#instagram-scraper-image").attr("src", "/static/progress/Check-Mark.png")

            $("#clarifai-loader").text("Analyzing Images...")
            $("#clarifai-loader-image").attr("src", "/static/progress/Loading.gif")
        } 
        $("#clarifai-loader-image").show()
    }

    function showEndProgress( needDelay ){
        if( needDelay ){
            //setTimeout(function(){
            //$("#clarifai-loader").text("clarifai (Done!)")
            $("#clarifai-loader-image").attr("src", "/static/progress/Check-Mark.png")
            //}, 5000)
        }
        else{
            //$("#clarifai-loader").text("clarifai (Done!)")
            $("#clarifai-loader-image").attr("src", "/static/progress/Check-Mark.png")
        }
        
    }

    // function toggleProgress( part, message ){
    //     if( part == 1 ){
    //         $("#instagram-scraper-loader").text(message)
    //     }
    //     else if( part == 2 ){
    //         $("#clarifai-loader").text(message)
    //     }
    // }
    function errorProgress( part, console_message ){
        if( part == 1 ){
            $("#instagram-scraper-image").attr("src", "/static/progress/Red-X.png")
            console.log(console_message)
        }
        else if( part == 2 ){
            $("#clarifai-loader-image").attr("src", "/static/progress/Red-X.png")
            console.log(console_message)
        }
    }
// ------------------ [ END ] Progress Functions ------------------




// ------------------ [START] Clearing Functions ------------------
    function clearEverything(){
        clearProgressSection()
        clearProfileSection()
        $("#username-error-display").text("")
    }

    function clearProfileSection(){
        clearTagSection()
        clearPhotoDisplaySection()
    }
    function clearProgressSection(){
        $("#instagram-scraper-loader").text("")
        $("#instagram-scraper-image").hide()
        $("#clarifai-loader").text("")
        $("#clarifai-loader-image").hide()
    }

    function clearTagSection(){
        $("#tag-section").hide()
        $("#tag-body").empty()
    }

    function clearPhotoDisplaySection(){
        $("#photo-display-section").hide()
        $("#photo-display-body").empty()
    }
// ------------------ [ END ] Clearing Functions ------------------



// ------------------ [START] Show Functions     ------------------
function showTagSection(){
    $("#tag-section").show()
}

function showPhotoDisplaySection(){
    $("#photo-display-section").show()
}
// ------------------ [ END ] Show Functions     ------------------


    //clearEverything()
    
    $("#search-btn-test").click(function(){
        clearEverything()
        showBeginningProgress()
        var username = $("#usernameField").val()
        beginPartOne( username )
    })
    
  });