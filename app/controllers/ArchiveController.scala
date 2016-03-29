package controllers

import javax.inject._
import play.api._
import play.api.mvc._

import scala.concurrent.Await
import scala.concurrent.duration.Duration.Inf

import models.{Curated, CuratedData}
import play.api.libs.json._

/**
  * Created by michael on 3/12/16.
  */
@Singleton
class ArchiveController @Inject() extends Controller {
  def showArchive = Action {
    Ok(views.html.archive())
  }

  def getData = Action {
    val curated = Await.result(CuratedData.getAll, Inf).toList
    Ok(Json.toJson(curated)(Curated.curatedSeqWrites))
  }
}


