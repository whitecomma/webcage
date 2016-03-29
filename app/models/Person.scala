package models

/**
  * Created by michael on 1/16/16.
  */

import scala.concurrent.Future
import com.websudos.phantom.dsl._

case class Person(id: Int, name: String)


class Persons extends CassandraTable[Persons, Person] {
  object id extends IntColumn(this) with PartitionKey[Int]
  object name extends StringColumn(this)

  def fromRow(row: Row): Person = {
    Person(
      id(row),
      name(row)
    )
  }
}

object Persons extends Persons with CassandraConnector {
  def store(person: Person): Future[ResultSet] = {
    insert.value(_.id, person.id).value(_.name, person.name)
      .consistencyLevel_=(ConsistencyLevel.ALL).future()
  }

  def getById(id: Int): Future[Option[Person]] = {
    select.where(_.id eqs id).one()
  }
}

