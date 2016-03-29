package controllers

import javax.inject._
import play.api._
import play.api.mvc._

import java.io.File

/**
 * This controller creates an `Action` to handle HTTP requests to the
 * application's home page.
 */
@Singleton
class HomeController @Inject() extends Controller {

  /**
   * Create an Action to render an HTML page with a welcome message.
   * The configuration in the `routes` file means that this method
   * will be called when the application receives a `GET` request with
   * a path of `/`.
   */
  def home = Action {
    Ok(views.html.home("Cage"))
  }

  def download(id: String, name: String) = Action {
    val fileWarehouse = "upfile"
    val fpath = s"$fileWarehouse/$id.zip"
    Ok.sendFile(
      content = new File(fpath),
      fileName = _ => s"$name.zip"
    )
  }

  def about = Action {
    Ok(views.html.about())
  }

}
