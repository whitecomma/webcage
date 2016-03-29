package models

/**
  * Created by michael on 1/21/16.
  */

import java.util.UUID

import org.joda.time.DateTime

import scala.concurrent.Future
import com.websudos.phantom.dsl._

case class Raw(
              id: UUID,
              species: String,
              cellType: String,
              lastUpload: DateTime,
              name: String,
              org: String,
              publication: String
              )

class RawData extends CassandraTable[RawData, Raw] {

  object id extends UUIDColumn(this) with PartitionKey[UUID]
  object species extends StringColumn(this)
  object cellType extends StringColumn(this)
  object lastUpload extends DateTimeColumn(this)
  object name extends StringColumn(this)
  object org extends StringColumn(this)
  object publication extends StringColumn(this)

  def fromRow(row: Row): Raw = {
    Raw(
      id(row),
      species(row),
      cellType(row),
      lastUpload(row),
      name(row),
      org(row),
      publication(row)
    )
  }
}

object RawData extends RawData with CassandraConnector {
  override val tableName = "raw"
  def store(r: Raw): Future[ResultSet] = {
    insert.value(_.id, r.id).value(_.species, r.species)
      .value(_.cellType, r.cellType)
      .value(_.lastUpload, r.lastUpload)
      .value(_.name, r.name).value(_.org, r.org)
      .value(_.publication, r.publication)
      .consistencyLevel_=(ConsistencyLevel.ALL).future()
  }

  def getById(id: UUID): Future[Option[Raw]] = {
    select.where(_.id eqs id).one()
  }

  def getAll(): Future[Seq[Raw]] = {
    select.fetch()
  }
}

