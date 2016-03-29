package models

/**
  * Created by michael on 1/17/16.
  */

import java.util.UUID

import scala.concurrent.Future
import com.websudos.phantom.dsl._

case class User(
               id: UUID,
               name: String,
               organization: String
               )

class Users extends CassandraTable[Users, User] {
  object id extends UUIDColumn(this) with PartitionKey[UUID]
  object name extends StringColumn(this)
  object organization extends StringColumn(this)

  def fromRow(row: Row): User = {
    User(
      id(row),
      name(row),
      organization(row)
    )
  }
}

object Users extends Users with CassandraConnector {
  override val tableName = "users"
  def store(user: User): Future[ResultSet] = {
    insert.value(_.id, user.id).value(_.name, user.name)
      .value(_.organization, user.organization)
      .consistencyLevel_=(ConsistencyLevel.ONE).future()
  }

  def getById(id: UUID): Future[Option[User]] = {
    select.where(_.id eqs id).one()
  }

  def getAll(): Future[Seq[User]] = {
    select.fetch()
  }
}
