package controllers


import javax.inject._
import play.api._
import play.api.mvc._

/**
  * Created by michael on 3/12/16.
  */

import java.io.File
import org.joda.time.DateTime

import models.{Raw, RawData}

@Singleton
class FileUploadController @Inject() extends Controller {
  val fileWarehouse = "upfile"
  def getUpload = Action {
    Ok(views.html.upload())
  }

  private def uuidGen(s: String) = {
    java.util.UUID.nameUUIDFromBytes(s.toCharArray map (_.toByte))
  }

  def postUpload = Action(parse.multipartFormData) { implicit request =>
    request.body.file("file") map { upf =>
      val ftype = upf.contentType.getOrElse("None")
      if (ftype != "application/zip") {
        Ok(views.html.upload("", null, "File Format must be zip"))
      } else {
        val orifname = upf.filename
        val species = request.body.dataParts("species")(0).trim
        val pub = request.body.dataParts("publication_sel")(0) match {
          case "Pub" => request.body.dataParts("publication")(0).trim
          case "UnPub" => "-"
        }
        val name = request.body.dataParts("name")(0).trim
        val org = request.body.dataParts("org")(0).trim
        val cell = request.body.dataParts("cell")(0).trim
        val uuid = uuidGen(s"$species$name$org$orifname")
        val fname = s"${uuid.toString}.zip"
        val lastUpload = new DateTime()

        val r: Raw = Raw(uuid, species, cell, lastUpload, name, org, pub)
        val f = new File(s"$fileWarehouse/$fname")
        if (f.exists) Ok(views.html.upload(orifname, r, "File exists"))
        else {
          upf.ref.moveTo(f)
          RawData.store(r)
          Ok(views.html.upload(orifname, r, s"$fname uploaded, $ftype"))
        }
      }
    } getOrElse {
      Ok("Upload Fail!")
    }
  }
}
