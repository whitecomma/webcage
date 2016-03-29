package models

/**
  * Created by michael on 3/14/16.
  */

import scala.concurrent.Future
import org.joda.time.DateTime

import com.websudos.phantom.dsl._

case class Model(
                cellType: String,
                refgem: String,
                source: String,
                fileName: String,
                lastUpdate: DateTime,
                metric: String,
                score: Double
                )

class ModelData extends CassandraTable[ModelData, Model] {
  object cellType extends StringColumn(this) with PartitionKey[String]
  object refgem extends StringColumn(this)
  object source extends StringColumn(this)
  object fileName extends StringColumn(this)
  object lastUpdate extends DateTimeColumn(this)
  object metric extends StringColumn(this)
  object score extends DoubleColumn(this)

  def fromRow(row: Row): Model = {
    Model(
      cellType(row),
      refgem(row),
      source(row),
      fileName(row),
      lastUpdate(row),
      metric(row),
      score(row)
    )
  }
}

object ModelData extends ModelData with CassandraConnector {
  override val tableName = "model"
  def store(m: Model): Future[ResultSet] = {
    insert.value(_.cellType, m.cellType)
      .value(_.refgem, m.refgem)
      .value(_.source, m.source)
      .value(_.fileName, m.fileName)
      .value(_.lastUpdate, m.lastUpdate)
      .value(_.metric, m.metric)
      .value(_.score, m.score)
      .consistencyLevel_=(ConsistencyLevel.ALL).future()
  }

  def getByCellType(c: String): Future[Option[Model]] = {
    select.where(_.cellType eqs c).one()
  }

  def getAll(): Future[Seq[Model]] = {
    select.fetch()
  }
}





