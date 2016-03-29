package controllers


import javax.inject._
import play.api._
import play.api.mvc._

import scala.concurrent.Await
import scala.concurrent.duration.Duration.Inf

/**
  * Created by michael on 3/14/16.
  */

import models.{Model, ModelData}
import models.{Curated, CuratedData}

@Singleton
class CasTest @Inject() extends Controller {
  def home = Action {
    //val m = Await.result(ModelData.getAll(), Inf).toList
    val m: Model = Await.result(ModelData.getByCellType("hela"), Inf).get
    //val m = Await.result(CuratedData.getAll(), Inf).toList
    Ok(m.toString())

  }
}
