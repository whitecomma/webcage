package controllers

import javax.inject._
import akka.util.ByteString
import play.api._
import play.api.http.HttpEntity
import play.api.mvc.BodyParsers.parse
import play.api.mvc._

import scala.concurrent.Await
import scala.concurrent.duration.Duration._
import java.io.File

/**
  * Created by michael on 3/13/16.
  */

import sys.process.Process
import models.{Model, ModelData}
import scala.io.Source

@Singleton
class EvalController @Inject() extends Controller {

  def sgEval(cellType: String) = Action {
    val m: Model = Await.result(ModelData.getByCellType(cellType), Inf).get
    Ok(views.html.sgeval(m))
  }

  def procFileEval() = Action(parse.multipartFormData) { implicit request =>
    val header = List("id", "chrom", "strand", "begin", "end", "sequence", "score").mkString("\t")
    val fileName = request.body.dataParts("fileName")(0).trim
    val refgem = request.body.dataParts("refgem")(0).trim
    request.body.file("file").map { upf =>
      val prefix = java.util.UUID.randomUUID().toString
      val fa = new File(s"/tmp/${prefix}.fa")
      upf.ref.moveTo(fa)
      val a = Process(s"python litecage/cage.py eval -f ${fa.getCanonicalPath} -m litecage/models/${fileName} -g ${refgem}").lineStream.iterator
      fa.delete()
      val b = s"${header}\n${a.toList.mkString("\n")}\n"
      Ok(b)
    }.getOrElse {
      Ok(s"${header}\n")
    }
  }

  def procCodEval() = Action(parse.multipartFormData) { implicit request =>
    val header = List("id", "chrom", "strand", "begin", "end", "sequence", "score").mkString("\t")
    val fileName = request.body.dataParts("fileName")(0).trim
    val refgem = request.body.dataParts("refgem")(0).trim
    val cod = request.body.dataParts("cod")(0).trim
    val direction = request.body.dataParts("direction")(0).trim
    val Array(codChr, codCod) = cod.split(":").map(_.trim)
    val Array(codBeg, codEnd) = codCod.split("-").map(_.trim)

    // For test  chr3: 195609062-195609284
    val a = Process(s"python litecage/cage.py eval -c $codChr -b $codBeg -e $codEnd -d $direction -m litecage/models/${fileName} -g ${refgem}").lineStream.iterator
    val b = s"${header}\n${a.toList.mkString("\n")}\n"
    Ok(b)
  }

}
