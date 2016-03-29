package models

/**
  * Created by michael on 1/21/16.
  */

import java.util.UUID

import org.joda.time.DateTime
import play.api.libs.json._

import scala.concurrent.Future
import com.websudos.phantom.dsl._

case class Curated(
                  id: UUID,
                  species: String,
                  cellType: String,
                  dataName: String,
                  lastUpdate: DateTime,
                  name: String,
                  org: String,
                  publication: String
                  ) {
  def toJson = {
    Json.toJson(this)(Curated.curatedWrites)
  }
}

object Curated {
  implicit val curatedWrites = new Writes[Curated] {
    def writes(c: Curated) = Json.obj(
      "id" -> c.id.toString,
      "species" -> c.species,
      "cellType" -> c.cellType,
      "dataName" -> c.dataName,
      "lastUpdate" -> c.lastUpdate.toString("yyyy-MM-dd"),
      "name" -> c.name,
      "org" -> c.org,
      "publication" -> c.publication
    )
  }

  implicit def curatedSeqWrites(implicit curated: Writes[Curated]): Writes[Seq[Curated]] = new Writes[Seq[Curated]] {
    def writes(lsc: Seq[Curated]) = JsArray(lsc map (c => curated.writes(c)))
  }

}

class CuratedData extends CassandraTable[CuratedData, Curated] {
  object id extends UUIDColumn(this) with PartitionKey[UUID]
  object species extends StringColumn(this)
  object cellType extends StringColumn(this)
  object dataName extends StringColumn(this)
  object lastUpdate extends DateTimeColumn(this)
  object name extends StringColumn(this)
  object org extends StringColumn(this)
  object publication extends StringColumn(this)

  def fromRow(row: Row): Curated = {
    Curated(
      id(row),
      species(row),
      cellType(row),
      dataName(row),
      lastUpdate(row),
      name(row),
      org(row),
      publication(row)
    )
  }
}

object CuratedData extends CuratedData with CassandraConnector {
  override val tableName = "curated"
  def store(cur: Curated): Future[ResultSet] = {
    insert.value(_.id, cur.id).value(_.species, cur.species)
      .value(_.cellType, cur.cellType)
      .value(_.dataName, cur.dataName)
      .value(_.lastUpdate, cur.lastUpdate)
      .value(_.name, cur.name).value(_.org, cur.org)
      .value(_.publication, cur.publication)
      .consistencyLevel_=(ConsistencyLevel.ALL).future()
  }

  def getById(id: UUID): Future[Option[Curated]] = {
    select.where(_.id eqs id).one()
  }

  def getAll(): Future[Seq[Curated]] = {
    select.fetch()
  }
}







